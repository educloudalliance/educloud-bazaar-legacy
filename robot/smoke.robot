*** Settings ***
Documentation  Test related to register a new user. Run with pybot --variable ENVIRONMENT:local_server --variable LANG:fi/en-gb register.robot
Resource  resources/${ENVIRONMENT}.robot
Suite setup  Open Browser and go to frontpage
Test Setup  Open frontpage
Suite Teardown  Close Browser

*** Variables ***


*** Test Cases ***

Accessing to server should be succesfull
	Open frontpage

Open Refine items should work
	Click Element  id=menu-categories
	Page Should Contain Link  Clear all

Search Should Work
	Input And Submit Search  homebrew
	Location Should Be  ${SERVER}/${LANG}/search/?q=homebrew
	Page Should Contain  Found 0 results


