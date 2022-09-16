@login
Feature: Login page

  @GWUAT-1
  Scenario: Check Login Page with Eyes
    Given a user wants to access the application
    Then  they are able to access the application


  @GWUAT-2
  Scenario: Check Login Page with OpenCV
    Given a user wants to access the application
    Then  they check application layout and compare with baseline


  @GWUAT-3
  Scenario: Compare partial screen (locator screenshot) with OpenCV
    Given a user wants to access the application
    When  they enter a correct username and correct password
    Then  they validate header on the landing page


  @GWUAT-4
  Scenario: Compare pdf report
    Given a pdf report


