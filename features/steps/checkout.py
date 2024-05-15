from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from behave import given, when, then
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import Select
import random

#Scenario: Proceeding to "Checkout" with qty. of item exceeding stock qty.
@given('shopping cart contains quantity of item exceeding stock quantity')
def step_given_shopping_cart_contains_quantity_of_item_exceeding_stock_quantity(context):
    context.driver.get('http://opencart:8080/en-gb/product/desktops/mac/imac')
    qty_input = context.driver.find_element(By.ID, "input-quantity")
    qty_input.clear()
    qty_input.send_keys("11100")
    context.driver.find_element(By.ID, "button-cart").click()

@when('browser is redirected to "Checkout" page')
def step_when_browser_is_redirected_to_checkout_page(context):
    context.driver.get("http://opencart:8080/en-gb?route=checkout/checkout")

@then('browser is redirected to "Shopping Cart" page')
def step_then_browser_is_redirected_to_shopping_cart_page(context):
   time.sleep(1)
   assert context.driver.current_url == 'http://opencart:8080/en-gb?route=checkout/cart'

@then('warning message is displayed')
def step_then_error_message_is_displayed(context):
    context.driver.implicitly_wait(5)
    warning = context.driver.find_element(By.CSS_SELECTOR, ".alert.alert-danger").text
    assert warning == "Products marked with *** are not available in the desired quantity or not in stock!"

#Scenario: Proceeding from "Shopping Cart" page to "Checkout"
@given('cart is not empty')
def step_given_cart_is_not_empty(context):
    context.driver.delete_all_cookies()
    context.driver.get('http://opencart:8080/en-gb/product/desktops/mac/imac')
    qty_input = context.driver.find_element(By.ID, "input-quantity")
    qty_input.clear()
    qty_input.send_keys("1")
    context.driver.find_element(By.ID, "button-cart").click()

@given('web browser is on "Shopping Cart" page')
def step_given_web_browser_is_on_shopping_cart_page(context):
    context.driver.get("http://opencart:8080/en-gb?route=checkout/cart")

@given('quantity of any item does not exceed stock quantity')
def step_given_quantity_of_any_item_does_not_exceed_stock_quantity(context):
    pass

@when('checkout button is clicked')
def step_when_checkout_button_is_clicked(context):
    context.driver.implicitly_wait(5)
    context.driver.find_element(By.XPATH, "//a[contains(text(), 'Checkout')]").click()


@then('browser is redirected to "Checkout" page')
def step_then_browser_is_redirected_to_checkout_page(context):
    print(context.driver.current_url)
    context.driver.implicitly_wait(5)
    assert context.driver.current_url == 'http://opencart:8080/en-gb?route=checkout/checkout'

#Scenario: Confirming order with some required fields not filled
@given('web browser is on the "Checkout" page')
def step_given_web_browser_is_on_the_checkout_page(context):
    context.driver.get("http://opencart:8080/en-gb?route=checkout/checkout")

@when('any of required fields is not filled')
def step_when_any_of_required_fields_is_not_filled(context):
    pass

@then('confirm order button cannot be clicked')
def step_then_confirm_order_button_cannot_be_clicked(context):
    context.driver.implicitly_wait(15)
    confirm_order_button =    context.driver.find_element(By.XPATH, "//button[contains(text(), 'Confirm Order')]")
    assert not confirm_order_button.is_enabled()

#Scenario: Confirming order 
@given('all required fields are filled')   
def step_given_all_required_fields_are_filled(context):
    context.driver.implicitly_wait(15)
    context.driver.find_element(By.ID, "input-firstname").send_keys("John")
    context.driver.find_element(By.ID, "input-lastname").send_keys("Doe")

    random_int = str(random.randint(10**(16-1), (10**16)-1))
    context.driver.find_element(By.ID, "input-email").send_keys(f"{random_int}@doe.john")
    context.driver.execute_script("window.scrollTo(0, 900);")
    time.sleep(1)
    context.driver.find_element(By.ID, "input-shipping-address-1").send_keys("Doe Street")
    context.driver.find_element(By.ID, "input-shipping-city").send_keys("Doe city")
    context.driver.find_element(By.ID, "input-shipping-postcode").send_keys("53011")
    context.driver.find_element(By.ID, "input-password").send_keys("53011")
    select_country = Select(context.driver.find_element(By.ID, "input-shipping-country"))
    select_country.select_by_visible_text("Uganda")
    select_country = Select(context.driver.find_element(By.ID, "input-shipping-zone"))
    select_country.select_by_visible_text("Arua")
    context.driver.find_element(By.ID, "input-register-agree").click()
    context.driver.find_element(By.ID, "button-register").click()
    context.driver.execute_script("window.scrollTo(0, 200);")
    time.sleep(1)
    context.driver.find_element(By.XPATH, '//button[contains(@id, "button-shipping-methods")]').click()
    context.driver.find_element(By.ID, "input-shipping-method-flat-flat").click()
    context.driver.find_element(By.XPATH, '//button[contains(@id, "button-shipping-method") and contains(text(), "Continue")]').click()
    context.driver.find_element(By.XPATH, '//button[contains(@id, "button-payment-methods")]').click()
    context.driver.find_element(By.ID, "input-payment-method-cod-cod").click()
    context.driver.find_element(By.XPATH, '//button[contains(@id, "button-payment-method") and contains(text(), "Continue")]').click()

@when('confirm order button is clicked')
def step_when_confirm_order_button_is_clicked(context):
    time.sleep(1)
    context.driver.find_element(By.XPATH, '//button[contains(text(), "Confirm Order")]').click()

@then('order is created')
def step_then_order_is_created(context):
    time.sleep(1)
    assert context.driver.find_element(By.CSS_SELECTOR, "h1").text == "Your order has been placed!"
  