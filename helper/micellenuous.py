from collections import OrderedDict, namedtuple

from datetime import datetime
from decimal import Decimal
import json, os
import string
import random
import faker
import csv
import re
import sys
from jsondiff import diff
from typing import List, Tuple
from dateutil.parser import parse
from calendar import monthrange
from screeninfo import get_monitors
from appium.webdriver.webdriver import WebDriver
from playwright.sync_api import Page


########################################################################################################
# helper function
########################################################################################################
def get_monitor_resolution():
    """
    usage : 
    resolution = get_monitor_resolution()
    if resolution:
        print(f"Current Monitor Resolution: {resolution[0]}x{resolution[1]}")
    else:
        print("Unable to retrieve monitor resolution.")
    """
    monitors = get_monitors()
    if monitors:
        monitor = monitors[0]  # Assuming the first monitor
        width = monitor.width
        height = monitor.height
        return width, height
    else:
        return None
    
"""
use to write a bytes[] of png to a file. 
"""


def bytetoFile(mybytes: bytes, filename: str):
    with open(filename, "wb") as binary_file:

        # Write bytes to file
        binary_file.write(mybytes)
    return True


"""
get the timetamp string to addup the file name
"""


def getTimestampStr()-> str:
    """
        get random time string 
    """
    dtobj = datetime.now(tz=None)
    return dtobj.strftime("%Y-%m-%d%H%M%S")
    # date_time_obj = datetime.strptime(str(datetime.now(tz=None)), '%Y-%m-%d%H:%M:%S')
    # return date_time_obj


def DictToTuple(obj):
    """converts given list or dict to named tuples, generic alternative to dataclass"""
    if isinstance(obj, dict):
        fields = sorted(obj.keys())
        namedtuple_type = namedtuple(
            typename="TestData",
            field_names=fields,
            rename=True,
        )
        field_value_pairs = OrderedDict(
            (str(field), DictToTuple(obj[field])) for field in fields
        )
        try:
            return namedtuple_type(**field_value_pairs)
        except TypeError:
            # Cannot create namedtuple instance so fallback to dict (invalid attribute names)
            return dict(**field_value_pairs)
    elif isinstance(obj, (list, set, tuple, frozenset)):
        return [DictToTuple(item) for item in obj]
    else:
        return obj


def parseJsonToTuple(file):
    """
    Read the content of the JSON file and convert it to a named tuple,
    can be used for injecting test data set to tests, helps in separating test data from the tests
    file : is a file , which will be inputted into the open(file) function. 
    """

    with open(file) as f:
        raw_data = json.load(f)
    return DictToTuple(raw_data)


def parseJsonToDict(file):
    with open(file) as f:
        raw_data = json.load(f)
        return raw_data
    return None

def remove_file_in_folder(foldername_path) : 
    """
    :foldername_path: the path to folder name
    """
    for the_file in os.listdir(foldername_path): 
        file_path = os.path.join(foldername_path, the_file) 
        try: 
            if os.path.isfile(file_path): 
                os.remove(file_path) 
        except Exception as e: 
            print(e)
# ====================================================================
# random the string
# ====================================================================
# from selenium.common.exceptions import WebDriverException


# def ScrollToAndClick(driver, selenium_element):
#     """ """
#     try:
#         driver.execute_script("arguments[0].scrollIntoView(true);", selenium_element)
#         driver.execute_script("arguments[0].click();", selenium_element)
#     except WebDriverException as e:
#         msg = (
#             f"Encountered an issue while attempting to execute script arguments[0].scrollIntoView(true);"
#             f"from {selenium_element}: {e.__class__.__name__}"
#         )
#         # raise common exception in python
#         raise ValueError(msg)


# ====================================================================
# random the string
# ====================================================================
def generate_Lower_string(length):

    # define the function and pass the length as argument
    # Print the string in Lowercase
    result = "".join(
        (random.choice(string.ascii_lowercase) for x in range(length))
    )  # run loop until the define length
    # print(" Random string generated in Lowercase: ", result)
    return result


def generate_Digit_string(length):
    result = "".join(
        (random.choice(string.digits) for x in range(length))
    )  # run loop until the define length
    return result


def generate_Mix_string(length):
    # get random password pf length 8 with letters, digits, and symbols
    characters = string.ascii_letters + string.digits + string.punctuation
    result = "".join(random.choice(characters) for i in range(length))
    return result


# from nltk.corpus import wordnet

# # generate a valid english word , and check if this word is valid english word. 
# def generate_Word(length : int=8) -> str :
#     """
#     generate a human readable word , but from a random set.
#     """
#     # Generate a random string of length 8


#     random_string = "".join(random.choices(string.ascii_lowercase, k=length))

# # Check if the string is a valid English word by using the WordNet corpus from NLTK
    
#     if wordnet.synsets(random_string):
#         print("Valid English Word:", random_string)
#     else:
#         print(f"{random_string} Not a Valid English Word")
#     return random_string


#python fucntion to generate text paragraph from "faker" package, the function input with specific length.
# the return : include special like . , !
# use function "remove_special_characters" to eliminate it. 
def generate_paragraph(length = 100) -> str :
    # fake = Faker()
    fake = faker.Faker()
    paragraph = fake.paragraph(nb_sentences=10 * length)
    return paragraph[0:length]

def generate_paragraph_without_special_char(length = 100):
    fake = faker.Faker()
    # paragraph = fake.text(max_nb_chars=length + length * 0.5)
    paragraph = fake.paragraph(nb_sentences=10 * length)
    return  remove_special_characters(paragraph)[0:length]

# python function input a string and it will eliminate the special char (but not space) out of the string. then it return the original string.
def remove_special_characters(string): 
    new_string = "" 
    for char in string: 
        if char.isalnum() or char==" ": 
            new_string += char 
    return new_string 

def compare_lists(list1: List[List], list2: List[List]) -> Tuple[List[List], List[List]]:
    """
    Compare two lists of lists and return their differences.
    compare item in order. 

    Args:
        list1 (List[List]): The first list of lists to compare.
        list2 (List[List]): The second list of lists to compare.

    Returns:
        A tuple containing the items that are unique to each list.

    Raises:
        ValueError: If either of the input lists is empty or None.
    USage : 
        if len(output) = 0 : two file is identical. 

    """
    if not list1 or not list2:
        raise ValueError("Both input lists must contain at least one item.")

    diff1 = diff(list1, list2)
    diff2 = diff(list2, list1)

    return diff1, diff2



def get_month_dates(date_str):
    """
    takes a string representing a date in ISO 8601 format as input. 
    It returns a tuple containing two strings representing the first and last dates of the month in which the input date falls.
    Example output : 
        ('01-Feb-2023', '28-Feb-2023')
    """
    dt = parse(date_str)
    year = dt.year
    month = dt.month
    _, last_day = monthrange(year, month)
    first_date = dt.replace(day=1).strftime('%d-%b-%Y')
    last_date = dt.replace(day=last_day).strftime('%d-%b-%Y')
    return first_date, last_date

class csvfile():
    """
    data : list of list, first row is header.
    Usage : 
        # filepath = "C:\\Mydata\\Proj-GlobalGis\\CDRfiles\\CDRFromGENARD\\CDRV3Input\\72000117GPRS20230304.csv.v3"

        # data = csvfile(filepath, delimiter='|')
        # print(data)
        # print(f"colum data RECORD_DATE_TIME = {data.get_column_data('RECORD_DATE_TIME')}")
        # print(f"cell data 1 of clumn {data.get_cell_data(1, 4)}")
    """
    _data = []

    def __init__(self, filepath, delimiter=',') -> None:
        self._filepath = filepath        
        self._delimiter = delimiter
        self._data = self.parse_csv_file()
        
    def __str__(self) -> str:
        return str(self._data)

    def parse_csv_file(self) -> list[list] :
        """
        Parse a CSV-like file with a specific delimiter and return a list of lists.
        """
        rows = []
        with open(self._filepath, 'r', newline='') as f:
            reader = csv.reader(f, delimiter=self._delimiter)
            for row in reader:
                rows.append(row)
        
        return rows

    def get_column_data(self, column_name):
        """
        Given a list of data with the first row as header, return a list
        of the values in the specified column for all rows.
        """
        column_index = self._data[0].index(column_name)
        return [row[column_index] for row in self._data[1:]]

    def get_cell_data(self, row_index, column_index):
        """
        Given a list of data, return the value at the specified row and column index.
        """
        return self._data[row_index][column_index]

    def get_cell_by_row_and_col_name(self, row_index, column_name):
        """
        Given a list of data with the first row as header, return the value
        at the specified row and column name.
        """
        column_index = self._data[0].index(column_name)
        return self._data[row_index][column_index]
    
    def get_datalist(self):
        return self._data
    
def smart_locator(locator, driver: Page|WebDriver):
    """
    This function takes two arguments: `locator` and `driver`. The `locator` argument can be either a string or a callable object. 
    The `driver` argument can be either a Page object in the playwright package or the driver of the appium package.
    If the `locator` argument is a string, it calls the `locator()` method of the `driver` object with the string as an argument. 
    If the `locator` argument is a callable object, it executes the callable object with the input of the page object.
    Before using any input arguments in your code, you should check them to ensure they are valid. If they are not valid, you should raise an exception.
    """
    if not isinstance(locator, str) and not callable(locator):
        raise TypeError("The locator must be a string or a callable object.")
    if not isinstance(driver, (Page, WebDriver)):
        raise TypeError("The driver must be a Page object in the playwright package or the driver of the appium package.")
    if isinstance(locator, str):
        if isinstance(driver, Page):
            return driver.locator(locator)
        if isinstance(driver, WebDriver):
            return api_findElement(driver=driver, locator= locator)
    else:
        if callable(locator):
            return locator(driver)
    

def api_findElement(driver: WebDriver, selector: str):
    """
    Find element by selector using Appium driver.

    Args:
        driver (WebDriver): Appium driver object.
        selector (str): Selector string specifying the element identification method.

    Returns:
        WebElement: Found element.

    Raises:
        ValueError: If the selector or driver is invalid.
    """
    matchfunc = {
        "" : ""
    }
    if not isinstance(driver, WebDriver):
        raise ValueError("Invalid driver")

    if not isinstance(selector, str) or not selector.strip():
        raise ValueError("Invalid selector")

    selector = selector.strip()

    # Pattern to identify the selector type
    access_word = ["accessibility_id","access"]
    pattern = r"^(id|name|class|xpath|accessibility_id|access):(.+)$"
    match = re.match(pattern, selector)
    
    if not match:
        raise ValueError("Invalid selector format")

    selector_type = match.group(1).lower()
    selector_value = match.group(2).strip()

    
    if selector_type == "id":
        return driver.find_element_by_id(selector_value)
    elif selector_type == "name":
        return driver.find_element_by_name(selector_value)
    elif selector_type == "class":
        return driver.find_element_by_class_name(selector_value)
    elif selector_type == "xpath":
        return driver.find_element_by_xpath(selector_value)
    elif selector_type in access_word:
        return driver.find_element_by_accessibility_id(selector_value)
    else:
        raise ValueError("Unsupported selector type")

def expand_string(reg_exp, func_name):
    def expanded_string(string):
        if re.match(reg_exp, string):
            return globals()[func_name]
        else:
            raise ValueError(f"String does not match the regular expression: {reg_exp}")
    
    return expanded_string

def convert_to_number(string):
    """
    convert3("1213324254354354354")
    1213324254354354354
    convert3("1213324254354354354.32443343")
    Decimal('1213324254354354354.32443343')
    convert3("12133242.54354354354")
    Decimal('12133242.54354354354')
    """
    # Remove commas from the string
    string = string.replace(',', '')

    # Check if the length of the string exceeds the maximum integer value
    if len(string) > len(str(sys.maxsize)):
        # Use Decimal for large numbers
        return Decimal(string)

    # Extract the decimal part (if any) using regular expression
    decimal_part = re.search(r'\.\d+', string)

    if decimal_part:
        # If a decimal part exists, replace the dot with an empty string
        string = string.replace('.', '', 1)
        return float(string[:decimal_part.start()] + '.' + string[decimal_part.start()+1:])

    # No decimal part, convert to int
    return int(string)

def convert_json_value(json_obj):
    for key, value in json_obj.items():
        if isinstance(value, dict):
            convert_json_value(value)
        elif isinstance(value, str):
            if value.lower() == "true":
                json_obj[key] = True
            elif value.lower()=="false":
                json_obj[key] = False
            elif value.isdigit() : 
                json_obj[key] = convert_to_number(value)
    return json_obj