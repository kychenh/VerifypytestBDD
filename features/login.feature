Feature: test login function
    Background: user access homepage
    Given user land on homepage
    
    Scenario: login with valid data
        Given user have a valid login username and password
        When user enter into username textbox
        And user enter password in password textbox.
        And user hit the submit button of login form.
        Then user should login successfully. 