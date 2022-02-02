from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
from random import randint
from bs4 import BeautifulSoup

def tripadvisor_scraper(city, number_of_pages=None, headless=True):
    """
    Function that returns a dictionary with the source of the scraped pages.

    Parameters:
    city (str): The city in Tripadvisor to be scraped.
    number_of_pages (int): The number of pages to be parsed (default None).
    headless (bool): Whether to show the Chrome browser controlled by Selenium or not (default True).

    Returns:
    dict: A dictionary with the page source for each parsed page.

    """

    # set the chrome driver options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")  # open Chrome in incognito mode

    if headless == True:
        chrome_options.add_argument("--headless")

    # create an instance of the browser
    browser = webdriver.Chrome(
        r".\ChromeDriver\chromedriver.exe", options=chrome_options)
    browser.get("https://www.tripadvisor.com")
    browser.maximize_window()

    # find the input space and enter the city name
    element = browser.find_element_by_xpath(
        '//input[@placeholder="Where to?"]')
    element.send_keys(city)
    # select the first entry from the dropdown list
    element.send_keys(Keys.ARROW_DOWN)
    # wait for the page to load and press enter
    time.sleep(randint(3, 5))
    element.send_keys(Keys.RETURN)

    # find the 'Things to Do' hyperlink and click
    time.sleep(randint(4, 6))
    element1 = browser.find_element_by_xpath('//a[@title="Things to Do"]')
    # click the element
    element1.click()

    # find the 'Activities' string and click
    time.sleep(randint(5, 8))
    element2 = browser.find_element_by_xpath(
        '//a[contains(string(),"Attractions")]')
    # click the element
    element2.click()

    # find the 'Activities' string and click it again, in case not selected yet
    time.sleep(randint(5, 8))
    element3 = browser.find_element_by_xpath(
        '//a[contains(string(),"Attractions")]')
    # click the element
    element3.click()

    # find the pages number and set its max value
    pages = browser.find_elements_by_xpath(
        '//a[@class="pageNum cx_brand_refresh_phase2 "]')
    page_values = [int(page.text) for page in pages]
    page_max = max(page_values)

    # check the max number of pages inputted by the user
    # set it equal to the max available in the website:
    # if not defined by the user
    if not number_of_pages:
        number_of_pages = page_max
    # or if larger than the max number of the page
    elif number_of_pages > page_max:
        number_of_pages = page_max

    # define a vocabulary where to store the page sources to convert into soup
    page_source_dict = {}

    for page in range(1, number_of_pages + 1):

        # scroll down to bottom of page to load all the page dynamically
        height_last = browser.execute_script(
            "return document.body.scrollHeight")

        while True:
            browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            # wait to load the content of the page
            time.sleep(4)
            height_new = browser.execute_script(
                "return document.body.scrollHeight")
            # stop if the page has reached the bottom (so newHeight == lastHeight)
            if height_new == height_last:
                break
            # set the new height equal
            height_last = height_new

        # click the next page
        if page != number_of_pages + 1:
            time.sleep(randint(4, 6))
            # append the page source to the dictionary
            page_source_dict[page] = browser.page_source
            print("Page {} out of {} has been successfully scraped and parsed".format(page, number_of_pages), end="\r")
            # click the next page
            element4 = browser.find_element_by_xpath(
                '//a[@class="ui_button nav next primary "]')
            element4.click()

        # break the loop once the requested amount of pages is reached
        elif page == number_of_pages + 1:
            break

    # close the browser
    browser.quit()

    print("\n")
    print("Scraping and parsing of {}'s Tripadvisor pages have been successfully performed".format(city))

    return page_source_dict


def landmarks_parser(page_source, landmarks_list=None):
    """
    Function that returns a dictionary with the points of interests found in the page sources.

    Parameters:
    page_source (dict): A dictionary with the page sources to be parsed.
    landmarks_list (list): A list containg the type of landmarks to be searched (default None).

    Returns:
    dict: The landmarks found that match the type(s) provided by the user.

    """
    
    # create the empy dictionary
    points_of_interest = {}

    # initiate the counter for the dictionary
    k = 1

    for i in range(1, len(page_source) + 1):

        # make the soup
        soup = BeautifulSoup(page_source[i], 'html.parser')
        # retrieve the different types of landmarks
        landmarks_type = soup.find_all("span", {"class": "_21qUqkJx"})
        # retrieve the different landmarks
        landmarks_selector = soup.find_all("h2")

        # for loop that create the landmark dict
        for j, ldmk_type in enumerate(landmarks_type):
            # check whether retrieve all landmarks or as provided by the user
            if not landmarks_list:
                points_of_interest[k] = {}
                points_of_interest[k]['name'] = str(landmarks_selector[j].text)
                # update the counter
                k += 1
            else:
                # insert the value in the dict if the landmark type matches those allowed
                if ldmk_type.text in landmarks_list:
                    # enumerate each poi and nestes a list in it
                    points_of_interest[k] = {}
                    points_of_interest[k]['name'] = str(landmarks_selector[j].text)
                    # update the counter
                    k += 1

    print("{} landmarks have been successfully inserted in the dictionary".format(k - 1))

    return points_of_interest


def info_scraper(points_of_interest, number_of_pois=None, headless=True):
    """
    Function that returns a dictionary with the required number of points of interests,
    their latitude & longitude and their Wikipedia description (latter two, if available).

    Parameters:
    page_source (dict): A dictionary with the landmark strings to be scraped.
    number_of_pois (int): The number of landmarks for which information must be scraped (default None).
    headless (bool): Whether to show the Chrome browser controlled by Selenium or not (default True).

    Returns:
    dict: A nested dictionary with each landmark's latitude & logitude and Wikipedia description (if available).
    """

    # creates a copy of the dictionary to avoid modifying the original one
    latlon_wiki_dict = points_of_interest.copy()

    # set the chrome driver options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")  # open Chrome in incognito mode

    if headless == True:
        chrome_options.add_argument("--headless")

    # create an instance of the browser
    browser = webdriver.Chrome(
        r"C:\ChromeDriver\chromedriver.exe", options=chrome_options)
    # fetch the URL
    browser.get("https://www.google.com")
    # maximize the Chrome windows
    browser.maximize_window()

    # change the language to English, if available
    try:
        language_choice = browser.find_element_by_xpath(
            '//a[contains(.,"English")]')  # string() instead of a dot not always work
        language_choice.click()

    except NoSuchElementException:
        print("Chrome is already in English or English is not available")
        print("\n")

    # set manually the max number of pages
    if not number_of_pois:
        number_of_pois = len(latlon_wiki_dict)
    elif number_of_pois > len(latlon_wiki_dict):
        number_of_pois = len(latlon_wiki_dict)
    else:
        for i in range(number_of_pois + 1, len(latlon_wiki_dict) + 1):
            # deletes the dictionary keys that are not required by the user
            del latlon_wiki_dict[i]

    for i in range(1, number_of_pois + 1):

        # set variables to None
        lat_lon = None
        desc_norm = None
        desc_err = None

        # set the string to be searched in the Google bar
        # composed by the landmark's name and its lat and long
        poi = latlon_wiki_dict[i]['name'] + ' latitude and longitude'

        # find the button to start the search and then click it
        search_bar = browser.find_element_by_xpath('//input[@class="gLFyf gsfi"]')
        search_bar.send_keys(poi)
        search_bar.send_keys(Keys.RETURN)

        # extract the coordinates and clean them
        time.sleep(randint(3, 6))
        try:
            lat_lon = browser.find_element_by_xpath('//div[@class="Z0LcW XcVN5d"]')

        # pass if the element could not be found
        except NoSuchElementException:
            pass

        # if the element has been found, it has the text attribute, which is not empty
        if lat_lon is not None and hasattr(lat_lon, "text") and lat_lon.text != "":
            coordinates = lat_lon.text.replace('°', ' ').split(' ')
            latlon_wiki_dict[i]['location'] = (
                float(coordinates[0]), -float(coordinates[3]))
        else:
            latlon_wiki_dict[i]['location'] = "NA"

        # retrieve the description
        try:
            # '//*' select all descendant (children and grandchildren)
            desc_norm = browser.find_element_by_xpath(
                '//div[@class="kno-rdesc"]//*')

        # if the element could not be found
        except NoSuchElementException:

            try:
                desc_err = browser.find_element_by_xpath('//span[@class="Yy0acb"]')
            except NoSuchElementException:
                latlon_wiki_dict[i]['description'] = "NA"

        # clean the formatting based on some common typologies
        if desc_norm is not None:
            latlon_wiki_dict[i]['description'] = desc_norm.text.replace(
                "Description\n", "").replace("Wikipedia", "")
        elif desc_err is not None:
            latlon_wiki_dict[i]['description'] = desc_err.text

        print("Landmark {} out of {} has been successfully scraped".format(i, number_of_pois), end="\r")

        # goes back to home page
        browser.execute_script("window.history.go(-1)")
        time.sleep(randint(3, 6))

    # close the browser once done
    browser.quit()

    print("\n")
    print("Scraping of coordinates and description has been successfully performed")

    return latlon_wiki_dict
