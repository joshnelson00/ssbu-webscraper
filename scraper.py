import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions() 
# Uncomment if you want headless mode
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')

service = Service(executable_path="./chromedriver")  # Adjust the path to chromedriver if necessary
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.start.gg/tournament/firefox-friday-120/attendees")

try:
    # Accept cookies first
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
    ).click()
    print("Accepted cookies.")
    time.sleep(5)

    gamer_tags = []
    while True:
        # Get page source and scrape the gamertags
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Scrape gamertags
        gamertags = soup.select('[data-test="gamertag"]')
        for gamertag in gamertags:
            print(gamertag.text)
            gamer_tags.append(gamertag.text)
        try:
            # Wait for the "Next" button to be clickable
            wait = WebDriverWait(driver, 10)

            # Use a more flexible selector for the next button
            next_button = wait.until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR, '.MuiPaginationItem-root[aria-label="Go to next page"]'
                ))
            )

            # Ensure it is visible and enabled
            if next_button.is_displayed() and next_button.is_enabled():
                next_button.click()  # Click the "Next" button
                print("------------------------------------------")
                time.sleep(3)  # Wait for the next page to load
            else:
                print("No more pages to navigate.")
                break  # Exit the loop if no more pages

        except Exception as button_error:
            print("Next button not found or clickable:", button_error)
            break  # Exit loop if there's an error with the button



except Exception as e:
    print("An error occurred:", e)



# *** TOTAL GAMER TAGS HERE ***
gamer_tags = sorted(gamer_tags)

print(gamer_tags)


# https://smashdata.gg/smash/ultimate/player/  HTTP BASE


for gamertag in gamer_tags:
    driver.get("https://smashdata.gg/smash/ultimate/player/")

    time.sleep(4)  # Wait for the page to load
    input_field = driver.find_element(By.ID, "search_tag")
    input_field.clear()  # Clear the input field before entering a new gamertag
    input_field.send_keys(gamertag)
    
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "ui-menu-item-wrapper"))
    ).click()
    
    time.sleep(3)  # Wait for the profile page to load

    





# Close the browser after the loop
# Perform Other/ Transferring Operations Here
driver.quit()


