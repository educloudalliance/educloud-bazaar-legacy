*** Settings ***
Documentation   Common variables and keywords
Library         Selenium2Library  0  implicit_wait=10    # Set explicit wait to 0 and implicit 

*** Variables ***


*** Keywords ***

Open Browser and go to frontpage
    Open Browser  ${SERVER}  ${BROWSER}
    Maximize Browser Window
    Location Should Be  ${SERVER}/${LANG}/

Open frontpage
    Go To  ${SERVER}/${LANG}/
    Location Should Be  ${SERVER}/${LANG}/

Open view
    [Arguments]  ${address}
    Go To  ${SERVER}/${address}
    Location Should Be  ${SERVER}/${address}/

Get unique email
  [Documentation]  Create a email that should not conflict with others
  [Arguments]  ${prefix}=user
  ${time}  Get time  epoch
  ${email}=  Catenate  SEPARATOR=  ${prefix}  .  ${time}  \@gmail.com
  [Return]  ${email}

Input registeration email
    [Arguments]  ${email}
    Input Text  id=id_registration-email  ${email}

Input registeration password
    [Arguments]  ${password}
    Input Password  id=id_registration-password1  ${password}
    Input Password  id=id_registration-password2  ${password}

Submit registeration form
    Click element  name=registration_submit

Setup variables
    ${email}=  Get unique email  basaar
    Set Suite Variable  ${EMAIL}  ${email}

Do Logout
    Click Link  Logout
    Location Should Be  ${SERVER}/${LANG}/

Open Profile View After Login
    Click Element  id=profile-icon
    Page Should Contain Link  Logout

Open language bar
    Click Element  xpath=//div[@id="language-icon"]//div[@class="menu-box"]
    Sleep  2 s

Select From Languages
    [Arguments]  ${val}
    Select From List By Value  name=language  ${val}

Input And Submit Search
    [Arguments]  ${search_val}
    Input Text  id=id_q  ${search_val}
    Press Key  id=id_q  \\13