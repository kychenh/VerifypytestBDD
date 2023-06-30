# Usage : 
# driver_factory = DriverFactory()
# driver = driver_factory.create_driver("web")
# driver_instance = driver.create_driver()
# driver.initialize_driver()

import abc

from appium import webdriver
from playwright.sync_api import (Page, BrowserContext, sync_playwright)


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
    """A factory for creating drivers."""

    def create_driver(self, testing_interface):
        """Creates a driver instance based on the input of a string of the testing interface."""

        if testing_interface == "web":
            return WebDriver()
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

class PlaywrightDriver:
    def __init__(self):
        self.browser: Page
        with sync_playwright() as playwright:
            self.browser = playwright.chromium.launch(headless=False).new_context().new_page()
        return self.browser

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


