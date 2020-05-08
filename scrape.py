from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import uuid
import os
import time


def scrape_matches(html_file):
    """Return list of dictionaries containing match records scraped from input html_file."""
    file = open(html_file, 'r')
    soup = BeautifulSoup(file, 'html.parser')
    matches = soup.find_all('flo-spotlight')
    records = []
    for match in matches:
        record = dict()
        record['uuid'] = uuid.uuid1()
        record['match_up'] = match.find('span', 'apply-text-hover').text
        record['date'] = match.find('p', 'subhead m-0 ng-star-inserted').text
        record['video_duration'] = match.find('span', 'video-duration hide-duration ng-star-inserted').text
        record['video_url'] = match.parent['href']
        record['belt'] = 'brown'
        records.append(record)
    return records


def scrape_image(matches):
    """Scrape image of match video."""
    base_url = 'https://www.flograppling.com'

    # Open chrome in full screen
    chrome_options = Options()
    chrome_options.add_argument("--start-fullscreen")
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

    # Start browser session and login
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(base_url + '/login')

    user_button = browser.find_element_by_css_selector('input[placeholder="Email Address"]')
    user_button.send_keys(os.environ.get('FLO_USERNAME'))

    password_button = browser.find_element_by_css_selector('input[placeholder="Password"]')
    password_button.send_keys(os.environ.get('FLO_PASSWORD'))

    submit_button = browser.find_element_by_css_selector('button[name="Login"]')
    ActionChains(browser).pause(5).move_to_element(submit_button).click().perform()

    # Loop through matches and extract screen shot
    for match in matches:
        browser.get(base_url + match['video_url'])
        browser.implicitly_wait(10)

        # Navigate to pause button and press
        pause_button = browser.find_element_by_css_selector('i[title="pause video"]')
        ActionChains(browser).pause(5).move_to_element(pause_button).click().perform()

        # Navigate to video progress bar, click & move it towards the end of the video
        progress_bar = browser.find_element_by_css_selector('div[id="progress-bar"]')
        ActionChains(browser).pause(5).drag_and_drop_by_offset(progress_bar, xoffset=350, yoffset=0).perform()

        # Press play and pause sequentially to reload frame
        play_button = browser.find_element_by_css_selector('i[title="play video"]')
        ActionChains(browser).pause(2).move_to_element(play_button).click().perform()
        ActionChains(browser).pause(1).move_to_element(pause_button).click().perform()

        # Enlarge screen and take a screen shoot
        full_screen_button = browser.find_element_by_css_selector('i[title="to fullscreen"]')
        ActionChains(browser).move_to_element(full_screen_button).pause(15).click().perform()

        # Take a screen shot
        browser.save_screenshot(f'screenshots/{match["uuid"]}.png')

    # close browser session
    browser.close()
    return


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


if __name__ == '__main__':
    matches = scrape_matches('brown_belts.html')
    chunk_generator = chunks(matches, 50)
    for chunk in chunk_generator:
        scrape_image(chunk)
        time.sleep(60 * 30)

