*** Settings ***
Resource  common_resources.robot
*** Variables ***
${PORT}  8000
${PROTOCOL}  http
${URL}  localhost
${SERVER}  ${PROTOCOL}://${URL}:${PORT}
${BROWSER}  firefox
${LANG}  fi