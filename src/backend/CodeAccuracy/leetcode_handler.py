import os
import logging

import json

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import xerox


LANGUAGE = "python3"


class LeetcodeHandler():
    def __init__(self, webdriver_path = None):
        self.logger = logging.getLogger()
        # create the selenium driver
        self.logger.debug("Starting Selenium driver")
        # if a different webdriver path is passed in use it, else use the default assets
        if webdriver_path:
            webdriver_path = webdriver_path
        else:
            webdriver_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'assets', 'chromedriver')
        self.driver = webdriver.Chrome(webdriver_path)


    def close_webdriver(self):
        self.driver.quit()

    def get_all_problems_urls(self, regenerate = False):
        """
        Retrieve all the available leetcode problems pages.

        Parameters:
            - driver (default: None): selenium driver used to scrape the most up to date number of pages

        Returns:
            - list of all the urls for the problems
        """
        leetcode_problems_url = "https://leetcode.com/problemset/all/"

        # if driver is passed in, we will scrape the most up to date number of pages
        # if driver is not passed in, we will use a hardcoded value that has been observed 
        # this value is 51 as of 12/18/2022
        if regenerate:
            self.driver.get(leetcode_problems_url)
            soup = BeautifulSoup(self.driver.page_source, features = "html.parser")
            navigation_container = soup.find("nav", {"role": "navigation"})
            navigation_buttons = navigation_container.find_all("button")
            last_button = navigation_buttons[-2]
            num_pages = int(last_button.text)
        else:
            num_pages = 51

        total_urls = []
        
        for page in range(1, num_pages + 1):
            total_urls.append(os.path.join(leetcode_problems_url, f"?page={page}"))
        
        return total_urls


    def parse_problems(self, url):
        base_url = "https://leetcode.com"
        
        self.driver.get(url)

        #enable the topics
        settings_button_id = self.driver.find_element(By.ID, "headlessui-popover-button-22")
        settings_button_id.click()
        topics_checkbox = settings_button_id.find_element(By.XPATH, "following-sibling::*[1]//*[1]//*[2]")
        topics_checkbox.click()

        soup = BeautifulSoup(self.driver.page_source, features="html.parser")
        table = soup.find("div", {"role": "table"})
        table_rows = table.find_all("div", {"role": "row"})
        result_rows = []
                
        for row in table_rows:
            cells = row.find_all("div", {"role": "cell"})
            # skips the header row
            if len(cells) > 0:
                title_link = cells[1].find("a")
                title_components = title_link.text.split(". ")
                problem_number = title_components[0]
                title = title_components[1]
                # remove the beginning slash of the url
                problem_url = os.path.join(base_url, title_link['href'][1:])
                locked = True if cells[1].find("svg") else False
                acceptance = cells[3].find("span").text
                difficulty = cells[4].find("span").text
                topic_tags = [tag.text.lower() for tag in cells[1].find_all("span")]
                
                # add to results
                self.logger.debug("Adding problem problem to result...\n\ttitle: %s", title)
                result_rows.append({
                    "title": title,
                    "problem_number": problem_number,
                    "problem_url": problem_url,
                    "acceptance": acceptance,
                    "difficulty": difficulty,
                    "locked": locked,
                    "topic_tags": topic_tags,
                })

        return result_rows


    def parse_problem_content(self, problem_url, language):
        # Note: The best way to get the header would be from the script with
        # id = __NEXT_DATA__, then retrieving the code snippets through
        # data = data["props"]["pageProps"]["dehydratedState"]["queries"][...]["state"]["data"]["question"]["codeSnippets"]
        # this would have allowed us to only use requests and be much faster / more efficient
        # the problem was that the script was returning inconsistently, only returning like 50%
        # we now use selenium to copy the content because you cant just grab the content as it is dynamically created on scroll
        # the problem content is grabbed from the selenium tag results as well 

        self.driver.get(problem_url)

        # problem_content = self.driver.find_element(By.XPATH, "//meta[@name='description']")
        # problem_content = problem_content.get_attribute('content')
        problem_content = WebDriverWait(self.driver, timeout = 15).until(lambda d: d.find_element(By.CSS_SELECTOR, "._1l1MA"))
        problem_content = problem_content.text


        self.set_problem_language(language)

        text_editor = WebDriverWait(self.driver, timeout = 25).until(lambda d: d.find_element(By.CSS_SELECTOR, ".view-lines.monaco-mouse-cursor-text"))

        text_editor.click()

        # have to use switch_to.active_element for this to work
        self.driver.switch_to.active_element.send_keys(Keys.COMMAND, "a")
        self.driver.switch_to.active_element.send_keys(Keys.COMMAND, "c")

        problem_header = xerox.paste()

        return (problem_header, problem_content)


    def set_problem_language(self, language):
        # get the language drop down
        language_dropdown_button =  WebDriverWait(self.driver, timeout = 15).until(lambda d: d.find_element(By.CSS_SELECTOR, "[id^='headlessui-listbox-button']"))
        language_dropdown_button.click()

        # get all the values of the language dropdown
        language_dropdown = language_dropdown_button.find_elements(By.XPATH, "following-sibling::*/li")
        language_dropdown_values = [t.text.lower() for t in language_dropdown]
        language_index = language_dropdown_values.index(language.lower())

        # click the desired language
        language_dropdown[language_index].click()


    def submit_problem(self, language, problem_url, openai_response):
        # must be logged in to submit

        # submit the result
        self.driver.get(problem_url)

        self.set_problem_language(language)

        # text_editor = WebDriverWait(self.driver, timeout = 25).until(lambda d: d.find_element(By.CSS_SELECTOR, ".view-lines.monaco-mouse-cursor-text"))
        text_editor = WebDriverWait(self.driver, timeout = 25).until(lambda d: d.find_element(By.XPATH, "//textarea"))
        text_editor.click()
        # wait until the editor is active or else the whole page gets selected
        WebDriverWait(self.driver, timeout = 25).until(lambda d: text_editor == d.switch_to.active_element)

        # have to use switch_to.active_element for this to work
        self.driver.switch_to.active_element.send_keys(Keys.COMMAND, "a")
        self.driver.switch_to.active_element.send_keys(Keys.BACKSPACE)
        sleep(1)
        
        # for some reason send_keys when using openai_response will indent the content improperly
        # use xerox to copy paste the content
        # dont not use copy paste when running this part or it will interfere 
        xerox.copy(openai_response)
        # xerox.copy(f"class Solution:\n\tdef twoSum(self, nums: List[int], target: int) -> List[int]:\n\t\treturn 0")
        self.driver.switch_to.active_element.send_keys(Keys.COMMAND, "v")

        submit_button = WebDriverWait(self.driver, timeout = 25).until(lambda d: d.find_element(By.XPATH, "//button[text()='Submit']"))
        submit_button.click()


        # succeed or fail check which element shows up
        result_element = WebDriverWait(self.driver, timeout = 60).until(lambda d: d.find_element(By.XPATH, "//*[contains(@class, 'text-xl font-medium text-red-s dark:text-dark-red-s') or contains(@class, 'flex w-full pb-4')]"))

        result_text = result_element.text.lower().split("\n")


        # success_responses = ["runtime", "beats", "memory"]
        # succeeded = all(success_message in result_text for success_message in success_responses)
        
        error_responses = ["runtime error", "wrong answer", "time limit exceeded"]
        succeeded = not any(error_message in result_text for error_message in error_responses)

        if succeeded:
            if len(result_text) > 4:
                memory = result_text[5].replace(" mb", "")
                memory_beats = result_text[7].replace("%", "")
            else:
                memory = None
                memory_beats = None
            solution_result = {
                "succeeded": succeeded,
                "runtime": int(result_text[1].replace(" ms", "")),
                "runtime_beats": result_text[3].replace("%", ""),
                "memory": memory,
                "memory_beats": memory_beats,
                "error_type": None,
                "error_message": None,
                "total_testcases": None,
                "testcases_passed": None
            }
        else:

            # get testcases passed
            testcases_element = WebDriverWait(self.driver, timeout = 15).until(lambda d: d.find_element(By.XPATH, "//*[text()='testcases passed']/span"))
            testcases_element = testcases_element.text.split(" / ")

            # get error message
            error_message = None
            if result_text[0] == "runtime error":
                error_message = WebDriverWait(self.driver, timeout = 15).until(lambda d: d.find_element(By.XPATH, "//*[contains(@class, 'whitespace-pre-wrap break-all font-menlo text-xs text-red-3 dark:text-dark-red-3')]")).text

            solution_result = {
                "succeeded": succeeded,
                "runtime": None,
                "runtime_beats": None,
                "memory": None,
                "memory_beats": None,
                "error_type": result_text[0],
                "error_message": error_message,
                "total_testcases": int(testcases_element[1]),
                "testcases_passed": int(testcases_element[0])
            }


        # return the solution
        return solution_result


    def login(self):
        # go to login page
        self.driver.get("https://leetcode.com/accounts/login/")

        # wait for spinner to disappear
        WebDriverWait(self.driver, timeout = 15).until_not(EC.presence_of_element_located((By.ID, "initial-loading")))
        
        # get all elements and enter login details
        email_login = WebDriverWait(self.driver, timeout = 15).until(lambda d: d.find_element(By.ID, "id_login"))
        email_login.send_keys(os.environ.get("LEETCODE_USER"))
        password_login = WebDriverWait(self.driver, timeout = 15).until(lambda d: d.find_element(By.ID, "id_password"))
        password_login.send_keys(os.environ.get("LEETCODE_PASSWORD"))
        login_button = WebDriverWait(self.driver, timeout = 15).until(lambda d: d.find_element(By.ID, "signin_btn"))
        login_button.click()

        # wait for the page to load after clicking login
        # login redirects to homepage with the storyboard so we will wait for that element
        WebDriverWait(self.driver, timeout = 15).until(lambda d: d.find_element(By.CLASS_NAME, "storyboard"))
