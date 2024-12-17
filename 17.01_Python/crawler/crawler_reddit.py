from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

service = Service("../17.03_Driver/geckodriver")
driver = webdriver.Firefox(service=service)
wait = WebDriverWait(driver, 10)

driver.get("https://old.reddit.com/r/nosleep/")

all_hrefs = []

try:
    while True:
        post_links = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'title.may-blank')))
        hrefs = [link.get_attribute('href') for link in post_links if link.get_attribute('href')]
        all_hrefs.extend(hrefs)

        try:
            next_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'next-button')))
            next_button.click()
        except:
            print("No more pages.")
            break

except Exception as e:
    print("An error occurred:", e)

finally:
    driver.quit()

# Writing to a CSV file
with open('../17.02_CSV.CSV/reddit_links_01_mars.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Links'])  # Writing header
    for href in all_hrefs:
        writer.writerow([href])

print("All links have been written")
