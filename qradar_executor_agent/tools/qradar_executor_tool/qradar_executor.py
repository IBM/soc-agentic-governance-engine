from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from ibm_watsonx_orchestrate.run import connections
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType

import json, ast
import requests

MY_APP_ID='qradar'


def build_qradar_headers(token) -> dict:
    return {
        "SEC": token,  # lowercase workaround
        "Accept": "application/json",
        "Version": "20.0",
        "Content-Type": "application/json"
    }

@tool(name="qradar_executor", description="Execute QRadar API", permission=ToolPermission.READ_ONLY, expected_credentials=[
        {"app_id": MY_APP_ID, "type": ConnectionType.KEY_VALUE}
    ]
)
def qradar_executor(endpoint, method, params, data, headers) -> str:

    creds = connections.key_value(MY_APP_ID)
    base_url = creds.get('base_url', '')
    sec_token = creds.get('sec_token', '')


    if not endpoint.startswith("/"):
        raise ValueError(f"❗ Invalid endpoint format: {endpoint}. It must start with `/`.")


    # 🛠️ Parse incoming strings into dicts if needed
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except Exception:
            data = {}

    if isinstance(params, str):
        try:
            params = json.loads(params)
        except Exception:
            params = {}

    if isinstance(headers, str):
        try:
            headers = ast.literal_eval(headers)
        except Exception:
            headers = {}

    # 🔧 Merge with default headers
    final_headers = build_qradar_headers(sec_token)
    # final_headers.update(headers)

    substring = "api"
    url = ''


    if substring in endpoint:
        url = f"{base_url}{endpoint}" 
    else:
        url = f"{base_url}/api{endpoint}" 


    response = requests.request(
        method=method,
        url=url,
        headers=final_headers,
        params=params or None,
        json=data or None,
        verify=False
    )

    if response.status_code >= 400:
        raise Exception(f"QRadar API Error {response.status_code}: {response.text}")
    
    return response.json()
