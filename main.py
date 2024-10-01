from selenium import webdriver
import os
import requests
from selenium.webdriver.common.by import By
import time



# Set up the web driver (make sure to download the appropriate driver for your browser)
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
driver.maximize_window()

def scrape_images(url, num_images, save_path):

    # Open the website
    driver.get(url)
    image_urls = []
    while True:
        images = driver.find_elements(By.TAG_NAME, 'img')
        image_urls = [image.get_attribute('src') for image in images]

        driver.execute_script("scrollBy(0, 300);")
        time.sleep(0.1)
        if len(image_urls) >= num_images:
            break
    # Create the directory to save the images
    # os.makedirs(save_path, exist_ok=True)
    save_path = save_path + '/'
    # Download the images
    for i, image_url in enumerate(image_urls[:num_images]):
        try:
            if "pexels" in image_url:
                image_url = image_url.split('?')[0]
                headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
                image = requests.get(image_url, headers=headers)
                with open(f'{save_path}{i}.jpeg', 'wb') as file:
                    file.write(image.content)
                    

                
        except Exception as e:
            print(e)
            


#get user input
query = input("Enter the query: ")
image_number = int(input("Enter the number of images: "))



scrape_images(f'https://www.pexels.com/search/{query}/', image_number, 'images')


# Close the web driver
driver.quit()
