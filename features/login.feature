Feature: test login function
    Background: user access homepage
    Given user land on homepage
    
    @login
    Scenario Outline: login with valid data
        Given user is on homepage
        When user enter into <username> textbox.
        And user enter <password> in password textbox.
        And user hit the submit button of login form.
        Then user should login successfully. 
        And user should see <Profiename> in profile menu. 
        Examples:
        |username | password | Profiename | 
        | mona.lisa@lelouvre.fr |  mona@Davensi123| Mona Lisa |

    @invalid @login
    Scenario Outline: login with invalid username or invalid password
        Given user is on homepage
        When user enter into <username> textbox.
        And user enter <password> in password textbox.
        And user hit the submit button of login form
        Then user see the error message appear in login form.
        And the error message is <err_msg>
        Examples:
        |username | password | err_msg | 
        |my.vo@dirox.net| klsjksldjf| user not found |
        
