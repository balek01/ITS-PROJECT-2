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
from selenium.common.exceptions import NoAlertPresentException


# Background: Login as admin
@given('web browser is loged in as admin')
def step_given_i_am_logged_in_as_admin(context):
    context.driver.get('http://opencart:8080/administration/')
    context.driver.implicitly_wait(15)
    context.driver.find_element(By.ID, 'input-username').send_keys('user')
    context.driver.find_element(By.ID, 'input-password').send_keys('bitnami')
    context.driver.find_element(By.ID, 'input-password').send_keys(Keys.ENTER)
    context.driver.implicitly_wait(15)
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
    context.driver.implicitly_wait(15)
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
    context.driver.implicitly_wait(15)
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

#Scenario Outline: Updating existing product and setting quantity to correct value
@then('quantity of product is updated to {correct}')
def step_then_quantity_of_product_is_updated(context, correct):
    context.driver.get(f'http://opencart:8080/administration/index.php?route=catalog/product&user_token={context.token}')
    context.driver.implicitly_wait(5)
    new_quantity = context.driver.find_element(By.XPATH, f"//input[@type='checkbox' and @value='42']/ancestor::tr//td[contains(@class, 'text-end')][2]").text
    assert new_quantity == correct

#Scenario Outline: Updating existing product and setting dimensions or weight to correct value
@when('dimensions or weight is modified to {correct} value')
def step_when_dimensions_or_weight_is_modified_to_correct_value(context, correct):
    context.driver.find_element(By.XPATH, '//a[@href="#tab-data"]').click()
    context.driver.execute_script("window.scrollTo(0, 900);")
    time.sleep(1)
    context.product_weight = context.driver.find_element(By.ID, 'input-weight').get_attribute('value')
    context.driver.find_element(By.ID, 'input-weight').clear()
    context.driver.find_element(By.ID, 'input-weight').send_keys(correct)

@then('changed properties of product are updated to {correct}')
def step_then_changed_properties_of_product_are_updated_to_correct(context, correct):
    context.driver.refresh()
    context.driver.implicitly_wait(5)
    context.driver.find_element(By.XPATH, '//a[@href="#tab-data"]').click()
    context.driver.execute_script("window.scrollTo(0, 900);")
    time.sleep(1)
    new_weight = context.driver.find_element(By.ID, 'input-weight').get_attribute('value')
    context.driver.refresh()
    print(new_weight)
    print(correct)
    assert float(new_weight) == float(correct)

#Scenario Outline: Updating existing product and setting dimensions or weight to incorrect value
@then('product weight is not updated')
def step_then_product_is_not_updated(context):
    context.driver.refresh()
    context.driver.implicitly_wait(5)
    context.driver.find_element(By.XPATH, '//a[@href="#tab-data"]').click()
    context.driver.execute_script("window.scrollTo(0, 900);")
    time.sleep(1)
    new_weight = context.driver.find_element(By.ID, 'input-weight').get_attribute('value')
    context.driver.refresh()
    print(new_weight)
    print(context.product_weight)
    assert float(new_weight) == float(context.product_weight)

#Scenario: Deleting existing product
@given('web browser is on the product list page')
def step_given_web_browser_is_on_the_product_list_page(context):
    context.driver.get(f'http://opencart:8080/administration/index.php?route=catalog/product&user_token={context.token}')

@when('any product is marked using checkbox')
def step_when_any_product_is_marked_using_checkbox(context):
    context.driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"][value="47"]').click()

@when('delete button is clicked')
def step_when_delete_button_is_clicked(context):
    context.driver.find_element(By.CSS_SELECTOR, 'button[title="Delete"]').click()

@then('confirmation message is shown')
def step_then_confirmation_message_is_shown(context):
    context.driver.implicitly_wait(5)
    try:
        alert = context.driver.switch_to.alert
        print(alert.text)
        assert alert.text == "Are you sure?"
    except NoAlertPresentException:
        assert False, "Alert not found."

@when('the user confirms deletion')
def step_when_the_user_confirms_deletion(context):
    context.driver.implicitly_wait(5)
    context.driver.switch_to.alert.accept()

@then('the item is deleted')
def step_then_the_item_is_deleted(context):
    context.driver.get(f'http://opencart:8080/administration/index.php?route=catalog/product&user_token={context.token}')
    context.driver.implicitly_wait(5)
    try:
        context.driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"][value="47"]')
        assert False, "Product not deleted"
    except NoSuchElementException:
        assert True, "Product deleted"

#Scenario: Adding new product
@given('web browser is on the add product page')
def step_given_web_browser_is_on_the_add_product_page(context):
    context.driver.get(f'http://opencart:8080/administration/index.php?route=catalog/product.form&user_token={context.token}')

@when('all required fields are filled correct information')
def step_when_all_required_fields_are_filled_correct_information(context):
    context.random_int = str(random.randint(10**(16-1), (10**16)-1))
    context.driver.find_element(By.ID, 'input-name-1').send_keys(f'1Ahooooj{context.random_int}')
    context.driver.find_element(By.ID, 'input-meta-title-1').send_keys(f'1Ahooooj{context.random_int}')
    context.driver.find_element(By.XPATH, '//a[@href="#tab-data"]').click()
    context.driver.find_element(By.ID, 'input-model').send_keys(f'1Ahooooj{context.random_int}')
    context.driver.find_element(By.XPATH, '//a[@href="#tab-seo"]').click()
    context.driver.find_element(By.ID, 'input-keyword-0-1').send_keys(f'1Ahooooj{context.random_int}')

@when('save button is clicked')
def step_when_save_button_is_clicked(context):
    context.driver.find_element(By.XPATH, "//button[@type='submit' and @class='btn btn-primary' and @title='Save']").click()

@then('new item is containing filled information is created')
def step_then_new_item_is_containing_filled_information_is_created(context):
    context.driver.get(f'http://opencart:8080/administration/index.php?route=catalog/product&user_token={context.token}')
    context.driver.implicitly_wait(5)
    td_element = context.driver.find_element(By.XPATH, f"//td[contains(text(), '1Ahooooj{context.random_int}')]")
    assert td_element is not None

#Scenario: Adding new product with incorrect information
@when('all required fieldsare are not filled')
def step_when_all_required_fields_are_filled_correct_information(context):
    context.random_int = str(random.randint(10**(16-1), (10**16)-1))
    context.driver.find_element(By.ID, 'input-name-1').send_keys(f'2Ahooooj{context.random_int}')


@then('new item is not created')
def step_then_new_item_is_not_created(context):
    context.driver.get(f'http://opencart:8080/administration/index.php?route=catalog/product&user_token={context.token}')
    context.driver.implicitly_wait(3)
    try:
        context.driver.find_element(By.XPATH, f"//td[contains(text(), '2Ahooooj{context.random_int}')]")
        assert False, "Product created"
    except NoSuchElementException:
        assert True, "Product not created"
