Feature: Checking out  

    Scenario: Proceeding to "Checkout" with qty. of item exceeding stock qty.
        Given shopping cart contains quantity of item exceeding stock quantity
        When browser is redirected to "Checkout" page
        Then browser is redirected to "Shopping Cart" page
        And warning message is displayed

    Scenario: Proceeding from "Shopping Cart" page to "Checkout"
        Given cart is not empty 
        And web browser is on "Shopping Cart" page
        And quantity of any item does not exceed stock quantity
        When checkout button is clicked
        Then browser is redirected to "Checkout" page

    Scenario: Confirming order with some required fields not filled
        Given cart is not empty 
        And web browser is on the "Checkout" page
        When any of required fields is not filled
        Then confirm order button cannot be clicked

    Scenario: Confirming order 
        Given cart is not empty
        And web browser is on the "Checkout" page
        And all required fields are filled
        When confirm order button is clicked
        Then order is created
