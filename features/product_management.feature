Feature: Managing products in administration

Background:
    Given web browser is loged in as admin

    Scenario: Updating existing product
	    Given web browser is on the edit product page
	    When all required fields are filled
        And update product button is clicked
	    Then product is updated accordingly to filled data

    Scenario: Updating existing product and not filling required fields
	    Given web browser is on the edit product page
	    When all required fields are not filled
        And update product button is clicked
	    Then warning message is shown
        And product is not updated
        

    Scenario Outline: Updating existing product and setting price to incorrect value
	    Given web browser is on the edit product page
	    When price is modified to <incorrect> value
        And update product button is clicked
	    Then warning message is shown
        And price of product is not updated 

        Examples:
        | incorrect |
        | -1233.23  |
        | abcd      |
        | 0.00      |
        | 123a12    | 

    Scenario Outline: Updating existing product and setting price to correct value
	    Given web browser is on the edit product page
	    When price is modified to <correct> value
        And update product button is clicked
	    Then price of product is updated to <correct>

        Examples:
        | correct   |
        | 1233.23   |
        | 16        | 

    Scenario Outline: Updating existing product and setting quantity to incorrect value
	    Given web browser is on the edit product page
	    When quantity is modified to <incorrect> value
        And update product button is clicked
	    Then warning message is shown
        And quantity of product is not updated 

        Examples:
        | incorrect   |
        | -123        |
        | 1.2         |  
        | abs         |

    Scenario Outline: Updating existing product and setting quantity to correct value
	    Given web browser is on the edit product page
	    When quantity is modified to <correct> value
        And update product button is clicked
	    Then quantity of product is updated to <correct>

        Examples:
        | correct   |
        | 123       |
        | 0         |

    Scenario Outline: Updating existing product and setting dimensions or weight to correct value
	    Given web browser is on the edit product page
	    When dimensions or weight is modified to <correct> value
        And update product button is clicked
	    Then changed properties of product are updated to <correct>

        Examples:
        | correct   |
        | 123       |
        | 0.123     | 

    
    Scenario Outline: Updating existing product and setting dimensions or weight to incorrect value
	    Given web browser is on the edit product page
	    When dimensions or weight is modified to <incorrect> value
        And update product button is clicked
	    Then warning message is shown
        And product is not updated 

        Examples:
        | correct   |
        | -123      |
        | 0.0       |
        | asdf      |           
             
    Scenario: Confirming deletion
        Given web browser is on the product list page
        When any product is marked using checkbox 
        And delete button is clicked
        Then confirmation message is shown
    
    Scenario: Deleting product
        Given the web browser is on the delete confirmation dialog
        When the user confirms deletion
        Then the item is deleted
        And the item is no longer visible in the list
    
    Scenario Outline: Adding new product
        Given web browser is on the add product page
        When all required <fields> are filled <correct> information
        And save button is clicked
        Then new item is containing filled information is created

        Examples:
        | fields            | correct   |
        | product name      | abc       |
        | meta tag title    | ooo       |
        | model             | akak      |
        | keyword           | asdasd    |
    
    Scenario: Adding new product with incorrect information
        Given web browser is on the add product page
        When all required fieldsare are not filled 
        And save button is clicked
        Then warning message is displayed
        And new item is not created


