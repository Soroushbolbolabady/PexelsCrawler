from selenium import webdriver
import os
import requests
from selenium.webdriver.common.by import By
import time
from concurrent.futures import ThreadPoolExecutor


def main():
    # Get user input
    query = input("Enter the query: ")
    image_number = int(input("Enter the number of images: "))
    save_path = input("Enter the path to save the images: ")
    scrape_images(f'https://www.pexels.com/search/{query}/', image_number, save_path)


def download_image(image_url, save_path, index):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        image = requests.get(image_url, headers=headers)
        with open(f'{save_path}{index}.jpeg', 'wb') as file:
            file.write(image.content)
    except Exception as e:
        print(f"Error downloading {image_url}: {e}")

def scrape_images(url, num_images, save_path):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    # Open the website
    driver.get(url)
    image_urls = set()  # Use a set to avoid duplicates
    downloaded_urls = set()  # Another set to track downloaded images

    # Create the directory to save the images
    save_path = save_path + '/'
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # Use ThreadPoolExecutor for parallel downloading
    with ThreadPoolExecutor() as executor:
        index = 0
        while len(downloaded_urls) < num_images:
            images = driver.find_elements(By.TAG_NAME, 'img')
            for image in images:
                image_url = image.get_attribute('src')
                if "pexels" in image_url:  # Ensure we are scraping relevant images
                    image_url = image_url.split('?')[0]  # Remove URL query parameters
                    if image_url not in image_urls:
                        image_urls.add(image_url)  # Add URL to the set of found URLs

                        # Start downloading the image only if it's not already downloaded
                        if image_url not in downloaded_urls:
                            downloaded_urls.add(image_url)
                            executor.submit(download_image, image_url, save_path, index)
                            index += 1

                            if len(downloaded_urls) >= num_images:
                                break

            driver.execute_script("scrollBy(0, 800);")
            time.sleep(0.1)  # Adjust for smoother scrolling

            print(f"Number of images found: {len(image_urls)}")

    # Close the web driver
    driver.quit()

if __name__ == '__main__':
    main()
