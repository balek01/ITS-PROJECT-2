Feature: Navigating trough products using category menu and searchbar

    Scenario: Opening category page from category menu 
	Given web browser is on the home page
	When user opens link in the category menu
        Then corresponding category page is opened

    Scenario: Searching for existing item using searchbar
        Given web browser is on the home page
        And items containing mac exists
	When user searches for mac
	Then search page with only items containing given mac is shown 
    
     Scenario: Searching for non-existent item using searchbar
	Given web browser is on the home page
        And items containing hesoiam does not exist
	When user searches for hesoiam
        Then search page with no hesoiam products is shown      
        