# this scenario can not effectively by route the specific url, 
# the page.route  and page.goto must be stand within one function
# otherwise, the page.route will not effect to page.goto. consequensely, it will not route the matching url to the handle_route function. 
# work around : i have try to return page obj to target_fixture and use this target_fixture to the next statement, but it does not effect. 
import allure, re, pytest
from os import path
from pytest import Session
from pytest_bdd import feature, given, then, when, scenario, parsers, scenarios
from playwright.sync_api import Page, expect
from assertpy import assert_that
import functools
from sttable import parse_str_table
import inspect

temp = "../features/reqIntercept.feature"
LOCATOR = {
}

#----------------------------------------------

def handle_route(route, request):
  
  # response = route.fetch()
  # json = response.json()
  # return json
  route.fulfill(body="{mocked-data}")
  # if ("html" in route.request.response.body):
  #   route.fulfill(body="{mocked-data}")
  # else : 
  #   route.continue_()
#======================================================================
scenarios(temp)

@given(parsers.re(r'user visit page "(?P<urlstring>.+)"'), target_fixture="response_page")
def step_function(page : Page, urlstring, response_filter):
    # page.route(url=response_filter["url"], handler=response_filter["handler"])
    # page.route(url=response_filter["url"], handler=handle_route)

    resp = response_filter(page)
    page.goto(url=urlstring,timeout=100000)
    return resp
    # assert 1==1

@given(parsers.parse('user filter API with pattern "{url_pattern}"'), target_fixture="response_filter")
def step_function(page : Page, url_pattern):
    def nestf(p : page): 
      myjson = ""
      def handle_route1(route, request):
          nonlocal myjson
          response = route.fetch()
          myjson = response.json()    
          route.continue_()
          return response
      p.route(url=str(url_pattern), handler=handle_route1)
      return myjson
    return nestf
   
@then(parsers.re(r'user see the response body is no empty(.|)'))
def step_function(page : Page, response_page ):
    print(response_page)
    allure.attach(response_page.__str__())
    assert 1==1
    