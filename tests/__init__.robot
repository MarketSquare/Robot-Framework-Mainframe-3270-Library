*** Settings ***
Resource          pub400_resources.txt
Suite Setup       Setup suite running
Suite Teardown    Close Connection    

*** Keywords ***
Setup suite running
    Create Directory    ${folder}
	Open Connection    ${host}