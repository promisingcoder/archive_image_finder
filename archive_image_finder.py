import requests
from bs4 import BeautifulSoup
from wayback import WaybackClient
import logging
import re
from datetime import datetime
from PIL import Image, ExifTags
from io import BytesIO
from urllib.parse import urljoin

logging.basicConfig(level=logging.DEBUG)

def get_archived_urls(domain, start_date, end_date, limit=None):
    client = WaybackClient()
    snapshots = client.search(domain, from_date=start_date, to_date=end_date)
    urls = [(snapshot.timestamp, snapshot.url) for snapshot in snapshots]
    if limit:
        urls = urls[:limit]
    return urls

def find_images_in_css(css_url, user_agent):
    headers = {'User-Agent': user_agent}
    response = requests.get(css_url, headers=headers)
    if response.status_code != 200:
        logging.error('Failed to retrieve CSS file: %s', css_url)
        return []

    css_content = response.text
    image_urls = re.findall(r'url\((.*?)\)', css_content)
    return [url.strip('\'"') for url in image_urls]

def find_images_in_archive(archive_url, user_agent):
    headers = {'User-Agent': user_agent}
    response = requests.get(archive_url, headers=headers)
    if response.status_code != 200:
        logging.error('Failed to retrieve archive page: %s', archive_url)
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    image_urls = [urljoin(archive_url, img['src']) for img in soup.find_all('img', src=True)]
    css_files = soup.find_all('link', rel='stylesheet', href=True)
    for css in css_files:
        css_url = urljoin(archive_url, css['href'])
        css_image_urls = find_images_in_css(css_url, user_agent)
        image_urls.extend([urljoin(css_url, img_url) for img_url in css_image_urls])

    return image_urls

def is_image_url(url):
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')
    return url.lower().endswith(image_extensions)

def get_image_timestamp(image_url, user_agent):
    headers = {'User-Agent': user_agent}
    response = requests.get(image_url, headers=headers)
    if response.status_code != 200:
        logging.error('Failed to retrieve image: %s', image_url)
        return None

    try:
        image = Image.open(BytesIO(response.content))
        exif_data = image._getexif()
        if exif_data:
            for tag, value in exif_data.items():
                if tag in ExifTags.TAGS and ExifTags.TAGS[tag] == 'DateTime':
                    return value
    except Exception as e:
        logging.error('Error extracting metadata from image: %s', e)
    
    return None

def main():
    domain = "harrys.com"
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    start_date = "2019-09-01"  # Expanded date range
    end_date = "2021-01-31"    # Expanded date range
    limit = 500000000  # Increased limit

    logging.debug('Fetching archived URLs for %s between %s and %s', domain, start_date, end_date)
    archived_urls = get_archived_urls(domain, start_date, end_date, limit)
    logging.debug('Found %d archived URLs', len(archived_urls))

    if not archived_urls:
        logging.error('No archived URLs found for the specified date range.')
        return

    images_with_dates = []

    for timestamp, archive_url in archived_urls:
        logging.debug('Checking archive URL: %s', archive_url)
        image_urls = find_images_in_archive(archive_url, user_agent)
        if image_urls:
            logging.debug('Found %d images in archive URL: %s', len(image_urls), archive_url)
            for img_url in image_urls:
                if is_image_url(img_url):
                    image_timestamp = get_image_timestamp(img_url, user_agent)
                    images_with_dates.append((img_url, archive_url, timestamp, image_timestamp))
                else:
                    logging.debug('Skipping non-image URL: %s', img_url)
        else:
            logging.debug('No images found in archive URL: %s', archive_url)

    if images_with_dates:
        with open('images_with_dates1.txt', 'w') as file:
            for img_url, archive_url, snapshot_timestamp, image_timestamp in images_with_dates:
                file.write(f"Image URL: {img_url} (from {archive_url}) on {snapshot_timestamp}, Image Timestamp: {image_timestamp}\n")
        print("Images with dates have been written to images_with_dates.txt")
    else:
        print("No images found in the specified date range.")

if __name__ == "__main__":
    main()
