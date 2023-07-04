Feature: verify ability to intercept the http request. #need do more implement step. 

    
    Scenario: capture a API response and compare later.
        Given user capture the response of API with pattern "**/uuid"
        And user visit page "https://httpbin.org/uuid"        
        Then user see the response body is no empty. 

        
    @runthis
    Scenario: intercept the API response
        Given user intercept API with url pattern "**/uuid" with data "{'moked-data' : '12121-12121-1212'}"
        And user capture the response of API with pattern "**/uuid"
        And user visit page "https://httpbin.org/uuid"
        Then user see the response body is "{'moked-data' : '12121-12121-1212'}"