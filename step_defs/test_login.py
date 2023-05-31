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


@given('user have a valid login username and password')
def step_function1(page : Page):
    # Add Your Code Here
    pass


@when(parsers.parse('user enter into username textbox'))
def step_function2(page : Page):
    page.get_by_placeholder("Enter your username").click()
    page.get_by_placeholder("Enter your username").fill("admin")
    # Add Your Code Here
    

@when(parsers.parse('user enter password in password textbox.'))
def step_function3(page : Page):
    page.get_by_placeholder("Enter your password").fill("Centralize123!")
    # Add Your Code Here
    

@when(parsers.parse('user hit the submit button of login form.'))
def step_function4(page : Page):
    # Add Your Code Here
    page.get_by_placeholder("Enter your password").press("Enter")
    

@then(parsers.parse('user should login successfully.'))
def step_function5(page : Page):
    # Add Your Code Here
    ProfileUserName = page.locator('div[class^="MenuProfile_UserName"]')
    expect(ProfileUserName).to_contain_text("Admin")
    

@given('user land on homepage')
def step_function(page: Page):
    # Add Your Code Here
    # page.set_default_navigation_timeout = 100000
    page.set_default_timeout = 100000
    page.goto("https://claims.centralize.equisoft.io/", timeout=100000) 
    
@given('user have an invalid login user and valid password')
def step_function(page: Page):
    # Add Your Code Here
    assert 1==1

@then('user see error message "invalid credential"')
def step_function(page: Page):
    # Add Your Code Here
    assert 1==1