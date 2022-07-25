from config import CONFIGS
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


class CHROME_Browser:
    """
    Class to use Browser.
    """

    def __init__(self):
        """
        Init browser settings.
        """
        self.driver = webdriver.Chrome(executable_path=CONFIGS.DRIVER)
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.url = None

    def open_page(self, url):
        """
        Open page in browser.
        :param url:
        """
        self.url = url
        self.driver.get(self.url)

    def get_element_text_by_id(self, el_id):
        """
        Get element text from page by id.
        :param el_id:
        :return:
        returns element text.
        """
        return self.driver.find_element(By.ID, el_id).text

    def quit(self):
        """
        Close the browser.
        """
        time.sleep(2)
        self.driver.quit()
