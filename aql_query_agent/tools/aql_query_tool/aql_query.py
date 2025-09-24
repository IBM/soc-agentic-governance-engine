from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from ibm_watsonx_orchestrate.run import connections
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType
import json, ast
import requests
import urllib.parse

MY_APP_ID='qradar'

@tool(name="aql_executor", description="Execute QRadar API", permission=ToolPermission.READ_ONLY, expected_credentials=[
        {"app_id": MY_APP_ID, "type": ConnectionType.KEY_VALUE}
    ])
def qradar_executor(query: str) -> str:

    creds = connections.key_value(MY_APP_ID)
    base_url = creds.get('base_url', '')
    sec_token = creds.get('sec_token', '')

    
    url = f"{base_url}/api/ariel/searches" 
    text = urllib.parse.quote(f"select LOGSOURCENAME(logsourceid), UTF8(payload) from events where LOGSOURCENAME(logsourceid) ILIKE '%{query}%' limit 1 last 10 minutes", safe= '')

    updated_url  = f"{url}?query_expression={text}"

    response = requests.request(
        method="POST",
        url=updated_url,
        headers={
            "SEC": sec_token,  # lowercase workaround
            "Accept": "application/json",
            "Version": "20.0",
            "Content-Type": "application/json"
        },
        verify=False
    )

    print('response', response)

    if response.status_code >= 400:
        raise Exception(f"❌ QRadar API Error {response.status_code}: {response.text}")

    search_id = response.json()['search_id']

    search_url = f"{base_url}/api/ariel/searches/{search_id}/results"

    res = requests.request(
        method="GET",
        url=search_url,
        headers={
            "SEC": sec_token,  # lowercase workaround
            "Accept": "application/json",
            "Version": "20.0",
            "Content-Type": "application/json"
        },
        verify=False
    )

    if res.status_code >= 400:
        raise Exception(f"❌ QRadar API Error {res.status_code}: {res.text}")
    
    result_payload = res.json()['events'][0]["utf8_payload"] if len(res.json()['events']) > 0 else "No log found"

    return result_payload

