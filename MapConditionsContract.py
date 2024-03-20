import requests

#-------------------------------------------------------------MAPPINGS--------------------------------------------------------------#

contract_mappings = [
    # Define your mappings here...
]

#------------------------------------------------------------PARAMETERS-------------------------------------------------------------#

auth_token = 'YOUR_AUTH_TOKEN_HERE'
URL = 'YOUR_CONTRACT_API_URL_HERE'
condition_set_URL = 'YOUR_CONDITION_SET_API_URL_HERE'

#-----------------------------------------------------------------------------------------------------------------------------------#

header = {'Authorization': 'Bearer ' + auth_token}

response = requests.get(condition_set_URL, headers=header)
condition_sets = response.json()

response2 = requests.get(URL, headers=header)
contracts = response2.json()

failures = []

# Update contracts with specified condition sets
for mapping in contract_mappings:
    condition_set_to_add = next((cs for cs in condition_sets if cs['name'] == mapping['conditionSetName']), None)
    contract_to_update = next((ct for ct in contracts if ct['necBillingCode'] == mapping['necBillingCode']), None)
    
    if condition_set_to_add and contract_to_update:
        response3 = requests.get(URL + contract_to_update['id'], headers=header)
        contract = response3.json()
        contract['conditionSetId'] = condition_set_to_add['id']
        final_response = requests.put(URL, json=contract, headers=header)
        print(final_response)
    else:
        failures.append(mapping['necBillingCode'] + '\t' + mapping['conditionSetName'])
        print(final_response.text)

print("Failures:", failures)
