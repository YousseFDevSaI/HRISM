import msal
import requests
from datetime import datetime
import logging
import json



def get_BC_token():
    authority_url = 'https://login.microsoftonline.com/159d77ac-d095-413e-a321-88480be90067'
    resource_url = 'https://api.businesscentral.dynamics.com'
    client_id = '.......'
    client_secret = '......'
    app = msal.ConfidentialClientApplication(client_id, client_credential=client_secret, authority=authority_url)
    result = app.acquire_token_by_username_password(scopes=[resource_url + '/.default'],password="......",username="......")
    return result['access_token']

def get_chart_of_accounts():
    
    access_token = get_BC_token()
    url = 'https://api.businesscentral.dynamics.com/v2.0/159d77ac-d095-413e-a321-88480be90067/ESLSCA-Sandbox/api/v2.0/companies(4a0fd2f7-1123-ef11-9f88-6045bd417043)/accounts'
    headers = {
        "Authorization" : f"Bearer {access_token}",
        "Content-Type" : "application/json",
        }
    
    response = requests.get(url, headers=headers)
    
    response_json = response.json()["value"]
    chart_of_accounts = [{"id" : account["id"], "displayName" : account["displayName"], "number" : account["number"]} for account in response_json]
    return chart_of_accounts
    
    