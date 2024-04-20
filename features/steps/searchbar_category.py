from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from behave import given, when, then
from selenium.webdriver.common.keys import Keys
  

#Scenario: Opening category page from category menu 
@given('Web browser is on the home page')
def step_given_browser_is_on_the_homepage(context):
    context.driver.get(context.base_url)

@when('User opens link in the category menu')
def step_user_clicks_on_the_category_menu(context):
    context.driver.find_element(By.CSS_SELECTOR, ".nav-link[href='http://opencart:8080/en-gb/catalog/software']").click()

@then('Corresponding category page is opened')
def step_then_coresponding_category_page_is_opened(context):
    context.driver.implicitly_wait(2)
    assert context.driver.current_url == context.base_url + "en-gb/catalog/software"

#Searching for existing item using searchbar
#assumses that testing database contains items with 'mac' string in their name
@given('items containing {string} exists')
def step_given_items_containing_string_exists(context,string):
    context.execute_steps('given Web browser is on the home page')
    pass

@when('user searches for {string}')
def step_user_searches_for_string(context, string):
    search_input = context.driver.find_element(By.NAME, "search")
    search_input.clear()
    search_input.send_keys(string)
    search_input.send_keys(Keys.RETURN)

@then('search page with only items containing given {string} is shown')
def step_then_search_page_with_only_items_containing_given_string_is_shown(context,string):
    context.driver.implicitly_wait(2)
    assert context.driver.current_url == context.base_url + "index.php?route=product/search&language=en-gb&search=" + string
    elements = context.driver.find_elements(By.CSS_SELECTOR, ".Description h4 a")
    for element in elements:
        if string not in element.text.lower():
            assert False, f"Item {element.text} does not contain '{string}' string"

#Scenario: Searching for non-existent item using searchbar
#assumses that testing database does NOT contains items with 'hesoiam' string in their name
@given('items containing {cc} does not exist')
def step_given_items_containing_string_does_not_exists(context, cc):
    context.execute_steps('given Web browser is on the home page')
    step_user_searches_for_string(context, cc)
   

@then('search page with no {string} products is shown')
def step_search_page_with_no_products_is_shown(context,string):
    context.driver.implicitly_wait(3)
    assert context.driver.current_url == context.base_url + "index.php?route=product/search&language=en-gb&search=" + string
    elements = context.driver.find_elements(By.CSS_SELECTOR, ".Description h4 a")
    print(elements)
    if elements:
        assert False, f"Page contains items: {elements}"
        

    