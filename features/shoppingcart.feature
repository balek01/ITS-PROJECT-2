Feature: Menaging in products shopping cart 

    Scenario Outline: Adding incorrect quantity of product to cart
        Given web browser is on page of specific product
        When <incorrect-input> is entered to "Qty" field
        And add to cart button is clicked
        Then number of items and the price in cart is not changed

        Examples:
                | incorrect-input   |
                | -12               |
                | abac              |
                | 0                 |
                | 1.2               |

    Scenario Outline: Adding correct quantity of product to empty cart
        Given web browser is on page of specific product
        And the price of the product is $122.00
        And the cart is empty
        When <correct-input> is entered to quantity field
        And add to cart button is clicked
        Then <number-of-products> and the <price> in cart is updated

        Examples:
                | correct-input     | number-of-products | price |
                | 12                | 12                 | 1464  |
                | 1                 | 1                  | 122   |
                | 3                 | 3                  | 366   |
    
    Scenario Outline: Adding item to empty cart from home page featured items
        Given web browser is on home page
        And the cart is empty
        When cart icon of item selling for <price> in featured items is clicked 
        Then number of items in cart is set to 1 and the price to <price>
    
         Examples:
                | price   | 
                | 602.00  |
                | 123.20  |

    
    Scenario Outline: Adding item to nonempty cart from home page featured items
        Given web browser is on home page
        And the cart is not empty
        When cart icon of item selling for <price> in featured items is clicked 
        Then number of items in cart is increased by 1 and the price by <price>
    
         Examples:
                | price   | 
                | 123.20  |
                | 602.00  |

    Scenario: Removing items from cart using the remove button
        Given the cart is not empty
        And web browser is on shopping cart page 
        When remove button is clicked
        Then item is removed from cart

    Scenario: Removing items from cart by changing its quantity to zero
        Given the cart is not empty 
        And web browser is on shopping cart page
        When quantity of prodct is set to zero
        And update button is clicked
        Then item is removed from cart    
    
    Scenario Outline: Updating quantity of product to correct value in cart page
        Given the cart is not empty 
        And web browser is on shopping cart page
        When <correct> input is entered to cart quantity field
        And update button is clicked
        Then quantity of updated item in cart is changed to <number> of products and the price to <price> 

        Examples:
                | correct | number | price |
                | 12      | 12     | 7224  |
                | 1       | 1      | 602   |
                | 3       | 3      | 1806  |

    Scenario Outline: Updating quantity of product to incorrect value in cart page
        Given the cart is not empty
        And web browser is on shopping cart page
        When <incorrect> input is entered to cart quantity field
        And update button is clicked
        Then quantity and price of products in cart is not changed

        Examples:
                | incorrect   |
                | -11         |
                | 2.5         |
                | asda        |

   
  
