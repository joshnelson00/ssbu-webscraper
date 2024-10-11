import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions() 
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')

service = Service(executable_path = "./chromedriver", chrome_options=options)
driver = webdriver.Chrome(service = service)

driver.get("https://www.start.gg/tournament/firefox-friday-120/attendees")

try:
    # Accept cookies first
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
    ).click()
    print("Accepted cookies.")
    time.sleep(5)

    while True:
        # Get page source and scrape the gamertags
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Scrape gamertags
        gamertags = soup.select('[data-test="gamertag"]')
        for gamertag in gamertags:
            print(gamertag.text)

        # Find the Next button
        next_button = driver.find_element(By.CSS_SELECTOR, 'button.MuiButtonBase-root.MuiPaginationItem-previousNext')

        # Check if the "Next" button is enabled
        if "Mui-disabled" not in next_button.get_attribute("class"):
            next_button.click()  # Click the "Next" button
            time.sleep(2)  # Wait for the next page to load
        else:
            print("No more pages to navigate.")
            break  # Exit the loop if no more pages

except Exception as e:
    print("An error occurred:", e)

# Close the browser after the loop
time.sleep(10)
driver.quit()