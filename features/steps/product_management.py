import random
from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from behave import given, when, then
from selenium.webdriver.common.keys import Keys
import time
from urllib.parse import urlparse, parse_qs
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchElementException


# Background: Login as admin
@given('web browser is loged in as admin')
def step_given_i_am_logged_in_as_admin(context):
    context.driver.get('http://opencart:8080/administration/')
    context.driver.find_element(By.ID, 'input-username').send_keys('user')
    context.driver.find_element(By.ID, 'input-password').send_keys('bitnami')
    context.driver.find_element(By.ID, 'input-password').send_keys(Keys.ENTER)
    assert context.driver.find_element(By.CSS_SELECTOR, 'div#content h1').text == 'Dashboard'
    parsed_url = urlparse(context.driver.current_url)
    query_params = parse_qs(parsed_url.query)
    context.token = query_params['user_token'][0]
    

#Scenario: Updating existing product
@given('web browser is on the edit product page')
def step_given_web_browser_is_on_the_edit_product_page(context):
    context.driver.get(f'http://opencart:8080/administration/index.php?route=catalog/product.form&user_token={context.token}&product_id=42')
  
@when('all required fields are filled')
def step_when_all_required_fields_are_filled(context):
    random_int = str(random.randint(10**(16-1), (10**16)-1))
    context.driver.find_element(By.ID, 'input-name-1').clear()
    context.driver.find_element(By.ID, 'input-name-1').send_keys(f'Ahooooj{random_int}')
    context.random_int = random_int

@when('update product button is clicked')
def step_when_update_product_button_is_clicked(context):
    context.driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)
    context.driver.find_element(By.XPATH, "//button[@type='submit' and @class='btn btn-primary' and @title='Save']").click() 
  
@then('product is updated accordingly to filled data')
def step_then_product_is_updated_accordingly_to_filled_data(context):
    context.driver.get(f'http://opencart:8080/administration/index.php?route=catalog/product&user_token={context.token}')
    context.driver.implicitly_wait(5)
    td_element = context.driver.find_element(By.XPATH, f"//td[contains(text(), 'Ahooooj{context.random_int}')]")
    assert td_element is not None

#Scenario: Updating existing product and not filling required fields
@when('all required fields are not filled')
def step_when_all_required_fields_are_not_filled(context):
    context.product_name = context.driver.find_element(By.ID, 'input-name-1').get_attribute('value')
    context.driver.find_element(By.ID, 'input-name-1').clear()


@then('warning message is shown')
def step_then_error_message_is_shown(context):
    context.driver.implicitly_wait(2)
    try:
        warning = context.driver.find_element(By.CSS_SELECTOR, ".alert.alert-danger").text
        assert warning == "Warning: Please check the form carefully for errors!"
    except NoSuchElementException:
        assert False, "Warning message not found."

@then('product is not updated')
def step_then_product_is_not_updated(context):
    context.driver.get(f'http://opencart:8080/administration/index.php?route=catalog/product&user_token={context.token}')
    context.driver.implicitly_wait(5)
    td_element = context.driver.find_element(By.XPATH, f"//td[contains(text(), '{context.product_name}')]")
    assert td_element is not None

#Scenario Outline: Updating existing product and setting price to incorrect value
@when('price is modified to {incorrect} value')
def step_when_price_is_modified_to_incorrect_value(context, incorrect):
    context.driver.find_element(By.XPATH, '//a[@href="#tab-data"]').click()
    context.driver.execute_script("window.scrollTo(0, 900);")
    time.sleep(1)
    context.product_price = context.driver.find_element(By.ID, 'input-price').get_attribute('value')
    context.driver.find_element(By.ID, 'input-price').clear()
    context.driver.find_element(By.ID, 'input-price').send_keys(incorrect)  

@then('price of product is not updated')
def step_then_price_of_product_is_not_updated(context):
    context.driver.get(f'http://opencart:8080/administration/index.php?route=catalog/product&user_token={context.token}')
    context.driver.implicitly_wait(5)
    new_price = context.driver.find_element(By.XPATH, f"//input[@type='checkbox' and @value='42']/ancestor::tr//td[contains(@class, 'text-end')][1]").text
    new_price = new_price.replace('$', '').replace(',', '').split('\n')[0]+"00"
    assert new_price == context.product_price

#Scenario Outline: Updating existing product and setting price to correct value    
@then('price of product is updated to {correct}')
def step_then_price_of_product_is_updated(context, correct):
    context.driver.get(f'http://opencart:8080/administration/index.php?route=catalog/product&user_token={context.token}')
    context.driver.implicitly_wait(5)
    new_price = context.driver.find_element(By.XPATH, f"//input[@type='checkbox' and @value='42']/ancestor::tr//td[contains(@class, 'text-end')][1]").text
    new_price = new_price.replace('$', '').replace(',', '').split('\n')[0]
    
    if '.00' in new_price:
        new_price = new_price.replace('.00', '')

    print(new_price)
    print(correct)
    assert new_price == correct

#Updating existing product and setting quantity to incorrect value
@when('quantity is modified to {incorrect} value')
def step_when_quantity_is_modified_to_incorrect_value(context, incorrect):
    context.driver.find_element(By.XPATH, '//a[@href="#tab-data"]').click()
    context.driver.execute_script("window.scrollTo(0, 900);")
    time.sleep(1)
    context.product_quantity = context.driver.find_element(By.ID, 'input-quantity').get_attribute('value')
    context.driver.find_element(By.ID, 'input-quantity').clear()
    context.driver.find_element(By.ID, 'input-quantity').send_keys(incorrect)

@then('quantity of product is not updated')
def step_then_quantity_of_product_is_not_updated(context):
    context.driver.get(f'http://opencart:8080/administration/index.php?route=catalog/product&user_token={context.token}')
    context.driver.implicitly_wait(5)
    new_quantity = context.driver.find_element(By.XPATH, f"//input[@type='checkbox' and @value='42']/ancestor::tr//td[contains(@class, 'text-end')][2]").text
    assert new_quantity == context.product_quantity