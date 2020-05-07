from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


def scrape_matches(html_file):
    """Return list of dictionaries containing match records scraped from input html_file."""
    file = open(html_file, 'r')
    soup = BeautifulSoup(file, 'html.parser')
    matches = soup.find_all('flo-spotlight')
    records = []
    for match in matches:
        record = dict()
        record['match_up'] = match.find('span', 'apply-text-hover').text
        record['date'] = match.find('p', 'subhead m-0 ng-star-inserted').text
        record['video_duration'] = match.find('span', 'video-duration hide-duration ng-star-inserted').text
        record['video_url'] = match.parent['href']
        record['belt'] = 'brown'
        records.append(record)
    return records


# Scrape matches data from static html file
matches = scrape_matches('brown_belts.html')

# Username and password for Flograppling
user_name = 'James.wash.56@gmail.com'
password = 'James56!'


# TODO Robust function capable of chucking up matches into batches and scrapping
browser = webdriver.Chrome()
for match in matches[132:-1]:
    # Initialize chrome webdriver & navigate to match example url
    base_url = 'https://www.flograppling.com'
    browser.get(base_url + match['video_url'])
    browser.implicitly_wait(10)

    # Workflow 1 - Navigate to pause button and press
    pause_button = browser.find_element_by_css_selector('i[title="pause video"]')
    ActionChains(browser).pause(5).move_to_element(pause_button).click().perform()

    # Workflow 2 - Navigate to video progress bar, click & move it towards the end of the video
    progress_bar = browser.find_element_by_css_selector('div[id="progress-bar"]')
    ActionChains(browser).pause(5).drag_and_drop_by_offset(progress_bar, xoffset=350, yoffset=0).perform()

    # Workflow 3 - Press play and pause sequentially to reload frame
    play_button = browser.find_element_by_css_selector('i[title="play video"]')
    ActionChains(browser).pause(2).move_to_element(play_button).click().perform()
    ActionChains(browser).pause(1).move_to_element(pause_button).click().perform()

    # Workflow 4 - Enlarge screen and take a screen shoot
    full_screen_button = browser.find_element_by_css_selector('i[title="to fullscreen"]')
    ActionChains(browser).move_to_element(full_screen_button).pause(5).click().perform()

    # Workflow 5 - Take a screenshot
    browser.save_screenshot(f'screenshots/{match["match_up"]}.png')

# close browser session
browser.close()
