from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

service = Service("17.03_Driver/geckodriver")  # Change to your actual path to the geckodriver
driver = webdriver.Firefox(service=service)
wait = WebDriverWait(driver, 10)

driver.get("https://creepypasta.fandom.com/wiki/Local_Sitemap?namefrom=%22De+Profundis%22")  # Change to the actual file path or URL

all_hrefs = []
visited_links = set()  # Set to keep track of visited links

try:
    while True:
        # Find all links within the "mw-allpages-chunk" element
        chunk_links = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.mw-allpages-chunk a')))
        hrefs = [link.get_attribute('href') for link in chunk_links if link.get_attribute('href')]
        all_hrefs.extend(hrefs)

        # Find navigation links (both previous and next page links)
        navigation_links = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.mw-allpages-nav a')))
        unvisited_navigation_links = [link for link in navigation_links if link.get_attribute('href') not in visited_links]

        if unvisited_navigation_links:
            # Assuming the last unvisited link is the 'Next page' link
            next_page_link = unvisited_navigation_links[-1]  # Change here to pick the last link
            visited_links.add(next_page_link.get_attribute('href'))  # Add this link to the set of visited links
            driver.execute_script("arguments[0].click();", next_page_link)
        else:
            print("No more new pages to visit.")
            break

except Exception as e:
    print("An error occurred:", e)

finally:
    driver.quit()

# Writing to a CSV file
with open('fandom_links.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Links'])  # Writing header
    for href in all_hrefs:
        writer.writerow([href])

print("All links have been written to fandom_links.csv")
