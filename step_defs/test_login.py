import allure
from os import path
from pytest import Session
from pytest_bdd import feature, given, then, when, scenario, parsers, scenarios
from playwright.sync_api import Page, expect


temp = "../features/login.feature"

scenarios(temp)

# @scenario(feature_name=FEATURE_FILENAME, scenario_name="login with valid data")
# def login_test():
#     print("finish login test!!!")
#     pass

@allure.step("user have a valid login username and password")
@given('user have a valid login username and password')
def step_function1(page : Page):
    # Add Your Code Here
    pass

@allure.step('user enter into username textbox')
@when(parsers.parse('user enter into username textbox'))
def step_function2(page : Page):
    page.get_by_placeholder("Enter your username").click()
    page.get_by_placeholder("Enter your username").fill("admin")
    # Add Your Code Here
    
@allure.step('user enter password in password textbox.')
@when(parsers.parse('user enter password in password textbox.'))
def step_function3(page : Page):
    page.get_by_placeholder("Enter your password").fill("Centralize123!")
    # Add Your Code Here
    
@allure.step('user hit the submit button of login form.')
@when(parsers.parse('user hit the submit button of login form.'))
def step_function4(page : Page):
    # Add Your Code Here
    page.get_by_placeholder("Enter your password").press("Enter")
    
@allure.step('user should login successfully.')
@then(parsers.parse('user should login successfully.'))
def step_function5(page : Page):
    # Add Your Code Here
    ProfileUserName = page.locator('div[class^="MenuProfile_UserName"]')
    expect(ProfileUserName).to_contain_text("Admin")
    
@allure.step('user land on homepage')
@given('user land on homepage')
def step_function(page: Page):
    # Add Your Code Here
    # page.set_default_navigation_timeout = 100000
    page.set_default_timeout = 100000
    page.goto("https://claims.centralize.equisoft.io/", timeout=100000) 
    