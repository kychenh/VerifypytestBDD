# Usage : 
# driver_factory = DriverFactory()
# driver = driver_factory.create_driver("web")
# driver_instance = driver.create_driver()
# driver.initialize_driver()

import abc

from appium import webdriver
from playwright.sync_api import (Page, BrowserContext, sync_playwright)

from playwright.async_api import async_playwright
import asyncio

class Driver(abc.ABC):
    """An abstract base class for drivers."""

    @abc.abstractmethod
    def create_driver(self):
        """Creates a driver instance."""
        pass

    @abc.abstractmethod
    def initialize_driver(self):
        """Initializes the driver instance."""
        pass

class DriverFactory(object):

    def __init__(self) -> None:
        pass
    """A factory for creating drivers."""

    def create_driver(self, testing_interface = "web"):
        """Creates a driver instance based on the input of a string of the testing interface."""

        if testing_interface == "web":
            return PlaywrightDriver()
        elif testing_interface == "mobile":
            return MobileDriver()
        elif testing_interface == "remote":
            return RemoteDriver()
        else:
            raise ValueError("Invalid testing interface: " + testing_interface)

class WebDriver(Driver):
    """A driver for web testing."""

    def create_driver(self):
        return "ChromeDriver"

    def initialize_driver(self):
        print("Initializing ChromeDriver...")

class MobileDriver(Driver):
    """A driver for mobile testing."""

    def create_driver(self):
        return "AppiumDriver"

    def initialize_driver(self):
        print("Initializing AppiumDriver...")

class RemoteDriver(Driver):
    """A driver for remote testing."""

    def create_driver(self):
        return "RemoteDriver"

    def initialize_driver(self):
        print("Initializing RemoteDriver...")

class PlaywrightDriver(Driver):
    def __init__(self):
        self.pw = None
        self.browser: Page = None


    def create_driver(self)->Page:
        if self.pw ==None : 
            raise Exception("no playwright fixture object")
            
        # with sync_playwright() as playwright:
        #     self.browser = playwright.chromium.launch(headless=False).new_context().new_page()
        # async with async_playwright() as p:
        #     tmp = await p.chromium.launch()
        #     self.browser = await tmp.new_page()

        tmp = self.pw.chromium.launch(headless=False).new_context()
        # self.set_browser(tmp.new_page())
        self.browser = tmp.new_page()
        
        return self

    def initialize_driver(self):
        print("Initializing PlaywrightDriver...")

    def set_pw(self, pw):
        self._pw = pw
        
    def get_pw(self):
        return self._pw
    
    def get_browser(self):
        return self._browser
    
    def set_browser(self, browser_obj):
        self._browser = browser_obj
        # self.browser = browser_obj

    browser = property(get_browser, set_browser)
    pw = property(get_pw, set_pw)

class AppiumDriver:
    def __init__(self):
        desired_caps = {
            "platformName": "Android",
            "platformVersion": "11",
            "deviceName": "emulator-5554",
            "appPackage": "com.android.calculator2",
            "appActivity": ".Calculator",
        }
        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)


