import allure, re, pytest
from os import path
from pytest import Session
from pytest_bdd import feature, given, then, when, scenario, parsers, scenarios
from playwright.sync_api import Page, expect
from assertpy import assert_that
import functools
from sttable import parse_str_table

urlstring = "https://httpbin.org/uuid"

myjson = ""
def handle_route(route, request):
    global myjson
    response = route.fetch()
    myjson = response.json()    
    route.continue_()
    return response
  
def resq_handler(response) : 
    print(response)
    print(response.body)
    return

def incercept_request(request):
    print("requested URL:", request.url)

def incercept_response(response):
    print(f"response URL: {response.url}, Status: {response.status}")

def intercept_requestfinish(request):
    print("requested URL:", request.url)
    print(f"response body: {request.response().json()}")

# @allure.step("test with out feature file")
# def test_nofeaturefile(page : Page):   
#     # intercept any request, match any url pattern. 
#     page.on("request", incercept_request)
#     page.on("response", incercept_response) 
#     page.on("requestfinished", intercept_requestfinish)

#     # intercept the request specific by url = url pattern , ex: **/getuser. 
    
#     page.route(url=urlstring, handler= handle_route)
#     print('set route successfully!')
#     page.goto(url=urlstring, timeout=100000)
   
#     print(f"iiid = {myjson}")

@allure.description("access google homepage!")
def test_google(idriver): 
    idriver.goto("http://www.google.com")   
    print(idriver)
    
    