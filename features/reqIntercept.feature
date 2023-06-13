Feature: verify ability to intercept the http request.

    @runthis
    Scenario: expect a response after event
        Given user filter API with pattern "**/uuid"
        And user visit page "https://httpbin.org/uuid"        
        Then user see the response body is no empty.  
        