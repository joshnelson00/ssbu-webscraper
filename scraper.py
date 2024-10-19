import time
from typing import Dict, List
from selenium import webdriver # type: ignore
from selenium.webdriver.chrome.service import Service # type: ignore
from selenium.webdriver.chrome.options import Options # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from bs4 import BeautifulSoup # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def get_gamertags(url: str):
    driver.get(url)

    try:
        # Accept cookies first
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        ).click()
        time.sleep(5)

        gamer_tags = []
        while True:
            # Get page source and scrape the gamertags
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # Scrape gamertags
            gamertags = soup.select('[data-test="gamertag"]')
            for gamertag in gamertags:
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
                    time.sleep(3)  # Wait for the next page to load
                else:
                    break  # Exit the loop if no more pages

            except Exception as button_error:
                print("Next button not found or clickable:", button_error)
                break  # Exit loop if there's an error with the button

    except Exception as e:
        print("An error occurred:", e)

    return sorted(gamer_tags)

def get_gamertag_data(gamer_tags: list[int]):
    # Initialize data for all players
    player_data = {}

    # Automate Query on Smash Data for each player
    for gamertag in gamer_tags:
        driver.get("https://smashdata.gg/smash/ultimate/player/")

        # Input and Search Gamertags when text box is found and emptied
        time.sleep(4)
        input_field = driver.find_element(By.ID, "search_tag")
        input_field.clear()
        input_field.send_keys(gamertag)

        # click first listing for player 
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "ui-menu-item-wrapper"))
        ).click()
        
        tournaments = driver.find_elements(By.CLASS_NAME, "tournament-listing")

        
        # Initialize data structures
        player = gamertag
        player_data[player] = {}
        dates = []
        events = []
        standings = []

        # Iterate through each tournament played and add data to the player's data
        for tournament in tournaments:
            date = tournament.find_element(By.CLASS_NAME, "date")

            

            event = tournament.find_element(By.CLASS_NAME, "name-rank")
            

            standing = tournament.find_element(By.CLASS_NAME, "placing")
            stripped_standing = standing.text.replace(" ", "")

            if date.text != "" and event.text != "" and stripped_standing != "":
                dates.append(date.text)
                events.append(event.text)
                standings.append(stripped_standing)

        # Assign data to player
        player_data[player]['dates'] = dates
        player_data[player]['events'] = events
        player_data[player]['standings'] = standings

    return player_data

def data_to_csv(tournament_data: Dict[str, Dict[str, List[str]]]):
    csv_data = []

    for gamertag, data in tournament_data.items():
        # Iterate over each set of data for a player
        for date, event, standing in zip(data['dates'], data['events'], data['standings']):
            # Append each set of data as a row
            csv_data.append({
                'gamertag': gamertag,
                'date': date,
                'event': event,
                'standing': standing,
            })

    with open('FFF_data.csv', mode='w', newline='') as file:
        pass  # Clean File 

    with open('FFF_data.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['gamertag', 'date', 'event', 'standing'])
        writer.writeheader()  # Write the header once
        writer.writerows(csv_data)  # Write all rows


#           Start of Program
# --------------------------------------

options = webdriver.ChromeOptions() 
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')

service = Service(executable_path="./chromedriver")  # Adjust the path to chromedriver if necessary
driver = webdriver.Chrome(service=service, options=options)




url = "https://www.start.gg/tournament/firefox-friday-121/attendees"

# gamer_tags = get_gamertags(url) # get gamertags

gamer_tags = ['ThatPossiblePog']
# Get data for every player
tournament_data = get_gamertag_data(gamer_tags)
data_to_csv(tournament_data)
time.sleep(5)

    





# Close the browser after the loop
# Perform Other/ Transferring Operations Here
driver.quit()


