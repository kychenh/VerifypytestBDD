import allure, re
from os import path
from pytest import Session
from pytest_bdd import feature, given, then, when, scenario, parsers, scenarios
from playwright.sync_api import Page, expect
from assertpy import assert_that
import functools
from sttable import parse_str_table
from helper.micellenuous import smart_locator

temp = "../features/login.feature"
baseURL = "https://davensi.dirox.dev"
LOCATOR = {
    "LOGINFORM" : ".login-form",
    "email" : lambda p : p.locator(LOCATOR["LOGINFORM"]).get_by_placeholder("email"), 
    "password" : 'password',
    "usreprofile" : '.header-topbar .user-dropdown',
    "err_msg" : ".error"
}


#======================================================================
scenarios(temp)

# @scenario(feature_name=FEATURE_FILENAME, scenario_name="login with valid data")
# def login_test():
#     print("finish login test!!!")
#     pass


@given('user have a valid login username and password')
def step_function1(idriver ):
    # Add Your Code Here
    pass


@when(parsers.re(r'user enter into (?P<username>.+) textbox(\.|)'))
def step_function2(idriver , username):
    email =    smart_locator(LOCATOR["email"], idriver)
    email.fill(username)
    # Add Your Code Here
    

@when(parsers.re(r'user enter (?P<password>.+) in password textbox(\.|)'))
def step_function3(idriver , password):
    ele = idriver.locator(LOCATOR["LOGINFORM"]).get_by_placeholder(LOCATOR["password"])
    ele.fill(password)    
   

@when(parsers.re(r'user hit the submit button of login form(\.|)'))
def step_function4(idriver ):    
    idriver.get_by_role("button", name="Login", exact=True).click()
    

@then(parsers.re(r'user should login successfully(\.|)'))
def step_function5(idriver ):
    # Add Your Code Here
    ProfileUserName = idriver.locator(LOCATOR["usreprofile"])
    ProfileUserName.wait_for(timeout=3000,state="visible")
    expect(ProfileUserName).not_to_be_empty()
    

@given('user land on homepage')
def step_function(idriver ):
    # Add Your Code Here
    # idriver.set_default_navigation_timeout = 100000
    idriver.set_default_timeout = 10000
    idriver.goto(baseURL, timeout=10000) 

@given(parsers.parse('user is on homepage'))
def step_f_user_is_on_homepage(idriver):
    assert idriver.locator(LOCATOR["LOGINFORM"]).is_visible()==True
    
@then(parsers.re(r'user should see (?P<Profiename>.+) in profile menu(\.|)'))
def step_function(idriver , Profiename):
    ProfileUserName = idriver.locator('.header-topbar .user-dropdown')
    ProfileUserName.wait_for(timeout=30000,state="visible")
    expect(ProfileUserName).to_contain_text(Profiename)

@then(parsers.re(r'\b(user|users|he|she|I)\b see the error message appear in login form(\.|)'))
def step_function(idriver ):
    errmsg_element = idriver.locator(LOCATOR["LOGINFORM"]).locator(LOCATOR["err_msg"])
    assert errmsg_element.is_visible() == True
    

# @then(parsers.re(r'the error message is "(?P<err_msg>.+)"'))
@then(parsers.parse('the error message is {err_msg}'))
def step_function(idriver, err_msg):
    errmsg_element = idriver.locator(LOCATOR["LOGINFORM"]).locator(LOCATOR["err_msg"])
    errmsg_element.wait_for(timeout=3000)
    expect(errmsg_element).to_have_text(re.compile(err_msg),ignore_case=True)
    

@when(parsers.parse("user enter username textbox:\n{mytable}"), target_fixture="username_table")
def step_function(idriver , datatable, mytable):
    # print(username)
    uname = parse_str_table(mytable)
    allure.attach(uname.columns.__str__())
    assert 1==1
    
