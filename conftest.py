import pytest
from browser import CHROME_Browser
from config import CONFIGS


@pytest.fixture(scope="function")
def open_browser():
    """
    Use this fixture to open browser before each test runs.
    :return:
    chrome driver
    """
    driver = CHROME_Browser()
    driver.open_page(CONFIGS.URL)
    return driver
