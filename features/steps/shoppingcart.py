import time
from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from behave import given, when, then
from selenium.webdriver.common.keys import Keys



#Scenario Outline: Adding incorrect quantity of product to cart
@given('web browser is on page of specific product')
def step_given_web_browser_is_on_page_of_specific_product(context):
    context.driver.get('http://opencart:8080/en-gb/product/desktops/mac/imac')
    context.items = context.driver.find_element(By.CSS_SELECTOR, "#header-cart button").text

@when('{incorrect_input} is entered to "Qty" field')
def step_when_incorrect_input_is_entered_to_qty_field(context, incorrect_input):
    context.driver.implicitly_wait(5)
    qty_input = context.driver.find_element(By.ID, "input-quantity")
    qty_input.clear()
    qty_input.send_keys(incorrect_input)

@when('add to cart button is clicked')
def step_when_add_to_cart_button_is_clicked(context):
    context.driver.find_element(By.ID, "button-cart").click()

@then('number of items and the price in cart is not changed')
def step_then_number_of_items_and_the_price_in_cart_is_not_changed(context):
    context.driver.find_element(By.CSS_SELECTOR, ".btn-close").click()
    items_new =context.driver.find_element(By.CSS_SELECTOR, "#header-cart button").text
    print(context.items)
    print(items_new)
    assert context.items == items_new


#Scenario Outline: Adding correct quantity of product to empty cart
@given('the price of the product is $122.00')
def step_and_the_price_of_the_product_is_122(context):
    context.execute_steps('given web browser is on page of specific product')

@given('the cart is empty')
def step_given_the_cart_is_empty(context):
    context.driver.delete_all_cookies()

@when('{correct_input} is entered to quantity field')
def step_when_correct_input_is_entered_to_quantity_field(context, correct_input):
    context.driver.implicitly_wait(5)
    qty_input = context.driver.find_element(By.ID, "input-quantity")
    qty_input.clear()
    qty_input.send_keys(correct_input)

@then('{number_of_products} and the {price} in cart is updated')
def step_then_number_of_products_and_the_price_in_cart_is_updated(context, number_of_products, price):
    context.driver.find_element(By.CSS_SELECTOR, ".btn-close").click()
    actual =context.driver.find_element(By.CSS_SELECTOR, "#header-cart button").text.replace(",","")
    expected= number_of_products + " item(s) - $" + price + ".00"
    assert actual == expected


#Scenario Outline: Adding item to empty cart from home page featured items
@given('web browser is on home page')
def step_given_web_browser_is_on_home_page(context):
    context.driver.get(context.base_url)
    context.execute_steps('given the cart is empty')

@when('cart icon of item selling for {price} in featured items is clicked')
def cart_icon_of_item_selling_for_price_in_fatured_items_is_clicked(context, price):
    context.driver.execute_script("window.scrollTo(0, 900);")
    time.sleep(1)
    button = context.driver.find_element(By.XPATH,f'//div[contains(@class, "product-thumb") and .//span[contains(@class, "price-new") and text()="${price}"]]//button[1]')
    button.click()

@then('number of items in cart is set to 1 and the price to {price}')
def step_then_number_of_items_in_cart_is_set_to_1_and_the_price_to_price(context, price):
    context.driver.implicitly_wait(5)
    context.driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)
    actual=context.driver.find_element(By.CSS_SELECTOR, "#header-cart button").text.replace(",","")
    expected= "1 item(s) - $" + price
    assert actual == expected

#Scenario Outline: Adding item to nonempty cart from home page featured items
@given('the cart is not empty')
def step_given_the_cart_is_not_empty(context):
    context.execute_steps('given web browser is on home page')
    context.driver.delete_all_cookies()
    context.driver.implicitly_wait(5)
    context.driver.execute_script("window.scrollTo(0, 1000);")
    time.sleep(2)
    button = context.driver.find_element(By.XPATH,f'//div[contains(@class, "product-thumb") and .//span[contains(@class, "price-new") and text()="$602.00"]]//button[1]')
    button.click()

@then('number of items in cart is increased by 1 and the price by {price}')
def step_then_number_of_items_in_cart_is_incremented_by_1_and_the_price_is_incremented_by_price(context, price):
    time.sleep(2)
    context.driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(2)
    actual = context.driver.find_element(By.CSS_SELECTOR, "#header-cart button").text.replace(",", "")
    expected_price = float(price) + 602.00
    expected = f"2 item(s) - ${expected_price:.2f}"
    print(actual)
    print(expected)
    assert actual == expected

#Scenario:Removing items from cart using the remove button

@given('web browser is on shopping cart page')
def step_given_web_browser_is_on_shopping_cart_page(context):
   time.sleep(2)
   context.driver.get('http://opencart:8080/en-gb?route=checkout/cart')
   
@when('remove button is clicked')
def step_when_remove_button_is_clicked(context):
    context.driver.implicitly_wait(5)
    context.driver.find_element(By.XPATH,"//button[2]/i").click()

@then('item is removed from cart')
def step_then_item_is_removed_from_cart(context):
        context.driver.implicitly_wait(5)
        actual = context.driver.find_element(By.CSS_SELECTOR, "#header-cart button").text
        expected = "0 item(s) - $0.00"
        assert actual == expected

#Scenario: Removing items from cart by changing its quantity to zero

@when('quantity of prodct is set to zero')
def step_when_quantity_of_product_is_set_to_zero(context):
    context.driver.implicitly_wait(5)
    qty_input = context.driver.find_element(By.CSS_SELECTOR, "#shopping-cart input")
    qty_input.clear()
    qty_input.send_keys("0")

@when('update button is clicked')
def step_when_update_button_is_clicked(context):
    context.driver.find_element(By.XPATH,"//*[@id='shopping-cart']/div/table/tbody/tr/td[4]/form/div/button").click()

#Scenario Outline: Updating quantity of product to correct value in cart page
@when('{correct} input is entered to cart quantity field')
def step_when_correct_input_is_entered_to_quantity_field(context, correct):
    context.driver.implicitly_wait(5)
    print(correct)
    qty_input = context.driver.find_element(By.CSS_SELECTOR, "#shopping-cart input")
    qty_input.clear()
    qty_input.send_keys(correct)

@then('quantity of updated item in cart is changed to {number} of products and the price to {price}')
def step_then_quantity_of_updated_item_in_cart_is_changed_to_number_of_products_and_the_price_to_price(context, number, price):
    actual = context.driver.find_element(By.CSS_SELECTOR, "#header-cart button").text.replace(",", "")
    expected = f"{number} item(s) - ${price}.00"
    print(actual)
    print(expected)
    assert actual == expected

#Scenario Outline: Updating quantity of product to incorrect value in cart page

@then('quantity and price of products in cart is not changed')
def step_then_quantity_and_price_of_products_in_cart_is_not_changed(context):
    context.driver.implicitly_wait(5)
    actual = context.driver.find_element(By.CSS_SELECTOR, "#header-cart button").text
    expected = "1 item(s) - $602.00"
    assert actual == expected