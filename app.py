import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def download_media(url, download_folder):
    # Create the download folder if it doesn't exist
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all image tags
    img_tags = soup.find_all('img')
    video_tags = soup.find_all('video')

    # Download images
    for img in img_tags:
        img_url = img.get('src') or img.get('data-src')
        if img_url:
            img_url = urljoin(url, img_url)  # Handle relative URLs
            img_name = os.path.basename(img_url)
            img_path = os.path.join(download_folder, img_name)

            try:
                img_data = requests.get(img_url).content
                with open(img_path, 'wb') as f:
                    f.write(img_data)
                print(f"Downloaded image: {img_name}")
            except Exception as e:
                print(f"Failed to download image {img_url}: {e}")

    # Download videos
    for video in video_tags:
        video_url = video.get('src') or video.get('data-src')
        if video_url:
            video_url = urljoin(url, video_url)  # Handle relative URLs
            video_name = os.path.basename(video_url)
            video_path = os.path.join(download_folder, video_name)

            try:
                video_data = requests.get(video_url).content
                with open(video_path, 'wb') as f:
                    f.write(video_data)
                print(f"Downloaded video: {video_name}")
            except Exception as e:
                print(f"Failed to download video {video_url}: {e}")


if __name__ == "__main__":
    # Example usage
    url = input("Enter the URL of the website: ")
    download_folder = "downloads"
    download_media(url, download_folder)