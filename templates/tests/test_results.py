from csv_file import CSV_File
import pytest
from config import CONFIGS, SELECTORS


def get_last_value():
    """
    Read last values from csv file to check info.
    :return:
    list of numbers[first_number, second_number].
    """
    csv_file = CSV_File(file_path=CONFIGS.CSV_PATH)
    return csv_file.read_csv(index=-1)


def test_check_number_in_csv_file(open_browser):
    """
    Run test to check is last generated values displayed on page.
    :param open_browser:
    Use fixture to open browser.
    """
    driver = open_browser
    second_number = driver.get_element_text_by_id(SELECTORS.SECOND_NUMBER)
    first_number = driver.get_element_text_by_id(SELECTORS.FIRST_NUMBER)
    last_value = get_last_value()
    assert last_value[0] == first_number
    assert last_value[1] == second_number
    driver.quit()


def test_is_first_number_higher_then_condition(open_browser):
    """
    Run test to check is first number higher than condition.
    :param open_browser:
    Use fixture to open browser.
    """
    driver = open_browser
    first_number = driver.get_element_text_by_id(SELECTORS.FIRST_NUMBER)
    assert int(first_number) > CONFIGS.CONDITION
    driver.quit()


@pytest.mark.parametrize("selector, start_range, end_range",
                         [(SELECTORS.FIRST_NUMBER, CONFIGS.FIRST_RANGE_LIMITS[0], CONFIGS.FIRST_RANGE_LIMITS[1]),
                          (SELECTORS.SECOND_NUMBER, CONFIGS.SECOND_RANGE_LIMITS[0], CONFIGS.SECOND_RANGE_LIMITS[1])])
def test_is_number_from_range(open_browser, selector, start_range, end_range):
    """
    Run test to check is number in range of each member of parameter list.
    :param open_browser:
    Use fixture to open browser.
    :param selector:
    Get Selector to use the correct number.
    :param start_range:
    Get minimal limit of range.
    :param end_range:
    Get maximum limit of range.
    """
    driver = open_browser
    driver.open_page()
    assert start_range <= int(driver.get_element_text_by_id(selector)) <= end_range
    driver.quit()
