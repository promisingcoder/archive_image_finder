# archive_image_finder


### Description:

The `archive_image_finder.py` script is designed to search for images on archived web pages within a specified date range. It leverages the Wayback Machine to retrieve archived URLs and then scans these pages for image files, including those referenced in CSS files. The script also attempts to extract timestamps from the images' metadata if available. The results, including image URLs and their associated timestamps, are written to a text file.

### Detailed Breakdown:

1. **Imports and Logging Configuration:**
   - The script imports necessary libraries such as `requests`, `BeautifulSoup`, `WaybackClient`, `logging`, `re`, `datetime`, `PIL`, `BytesIO`, and `urljoin`.
   - Logging is configured to the DEBUG level to capture detailed information during execution.

2. **Function Definitions:**
   - `get_archived_urls(domain, start_date, end_date, limit=None)`: 
     - Uses the WaybackClient to search for archived snapshots of a given domain within a specified date range.
     - Returns a list of tuples containing the timestamp and URL of each snapshot.
   
   - `find_images_in_css(css_url, user_agent)`:
     - Fetches a CSS file and extracts image URLs referenced within it.
     - Returns a list of image URLs found in the CSS file.
   
   - `find_images_in_archive(archive_url, user_agent)`:
     - Fetches an archived web page and parses it using BeautifulSoup.
     - Extracts image URLs from `<img>` tags and CSS files linked in the page.
     - Returns a list of image URLs found on the page and in its CSS files.
   
   - `is_image_url(url)`:
     - Checks if a URL points to an image file based on its extension.
     - Returns `True` if the URL ends with a known image extension, otherwise `False`.
   
   - `get_image_timestamp(image_url, user_agent)`:
     - Fetches an image and attempts to extract its timestamp from the EXIF metadata.
     - Returns the timestamp if found, otherwise `None`.

3. **Main Function:**
   - Defines the domain, user agent, date range, and limit for the search.
   - Fetches archived URLs for the specified domain and date range.
   - Iterates through each archived URL, finding and processing images.
   - Extracts timestamps from images and compiles a list of results.
   - Writes the results to a text file named `images_with_dates1.txt`.

4. **Execution:**
   - The script's main function is executed if the script is run as the main module.

### Usage:
To use this script, simply run it in a Python environment. Ensure that all required libraries are installed. The script will output a text file containing the URLs of images found on archived pages, along with their associated timestamps if available.

### Example Command:
```bash
python archive_image_finder.py
```

This script is useful for researchers, historians, or anyone interested in tracking the visual content of a website over time using archived snapshots.
