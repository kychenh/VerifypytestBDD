# this scenario can not effectively by route the specific url, 
# the page.route  and page.goto must be stand within one function
# otherwise, the page.route will not effect to page.goto. consequensely, it will not route the matching url to the handle_route function. 
# work around : i have try to return page obj to target_fixture and use this target_fixture to the next statement, but it does not effect. 

#todo : lookup todo in this file to do it. 
import allure, re, pytest
from os import path
from pytest import Session
from pytest_bdd import feature, given, then, when, scenario, parsers, scenarios
from playwright.sync_api import Page, expect
from assertpy import assert_that
import functools
from requests import Response
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
  # route.fulfill(body=idata)
  
  # if ("html" in route.request.response.body):
  #   route.fulfill(body="{mocked-data}")
  # else : 
  #   route.continue_()
#======================================================================
scenarios(temp)

@given(parsers.re(r'user visit page "(?P<urlstring>.+)"'))
def step_function(page : Page, urlstring):
    # page.route(url=response_filter["url"], handler=response_filter["handler"])
    # page.route(url=response_filter["url"], handler=handle_route)

    # resp = response_filter(page)
    page.goto(url=urlstring,timeout=100000)
    return None
    # assert 1==1

idata = None
def handle_response(response) : 
   global idata
   idata = response
   return response

@given(parsers.parse('user capture the response of API with pattern "{url_pattern}"'))
def step_function(page : Page, url_pattern):
    page.on('response', handle_response)

@then(parsers.re(r'user see the response body is no empty(.|)'))
def step_function(page : Page ):
    print(f"response by idata = {idata} and json = {idata.json()}")
    if idata==None: 
       raise ValueError("exchange variable 'idata' does not have value, idata={idata}")
    assert_that(idata.json()).is_not_empty()


# @given(parsers.parse('user capture the response of API with pattern "{url_pattern}"'), target_fixture="response_page")
# def step_function(page : Page, url_pattern):
#     page.on('response', handle_response)
    
#     def nestf(p : page): 
#       myjson = ""  # todo : currently this value always return null. 
      
#       def handle_route1(route, request):
#           nonlocal myjson
#           response = route.fetch()
#           myjson = response.json()    
#           route.continue_()
#           return response
#       p.route(url=str(url_pattern), handler=handle_route1)
#       return myjson
#     return nestf(page)
   
# @then(parsers.re(r'user see the response body is no empty(.|)'))
# def step_function(page : Page, response_page ):
#     print(f"\nresponse_page = {response_page}")  # print :  <function step_function.<locals>.nestf at 0x000002170A203400>
#     print(f"response by idata = {idata} and json = {idata.json()}")
#     #todo : 
#     # try to get 'json' to verify the response. 
#     allure.attach(response_page.__str__())
#     assert 1==1
    
@then(parsers.parse('user see the response body is "{data}"'))
def step_user_see_response_body_is_data(page : Page, data):
    print(f"compare idata {idata.text()} with \nvar data {data}")
    if idata==None: 
       raise ValueError("exchange variable 'idata' does not have value, idata={idata}")
    
    assert_that(idata.text()).is_not_empty()
    assert_that(idata.text()).contains(data)
    


@given(parsers.parse('user intercept API with url pattern "{url_pattern}" with data "{mockdata}"'), target_fixture="mockdata")
def step_function(page : Page, url_pattern, mockdata, request):
    def tmp_handle_route(route, request):
      route.fulfill(body=mockdata)
    page.route(url=url_pattern, handler=tmp_handle_route)
    print(f"mockdata = {mockdata}")
    