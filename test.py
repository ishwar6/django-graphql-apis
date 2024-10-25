import requests
import pandas as pd


def get_access_token(tokens_url, client_id, client_secret, scope):
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': scope
    }
    
    response = requests.post(tokens_url, data=data)
    if response.status_code == 200:
        print("Access Token generated successfully")
        token_data = response.json()
        access_token = token_data.get("access_token")
        return access_token
    else:
        print(f"Failed to generate token: {response.status_code}")
        print(response.text)
        return None
 
def get_data_from_search_api(api_url, access_token, search_key, user_email):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    payload = {
        "keyword": search_key,
        "facets": [
            {"id": "domain", "field": "container.domain_facet_field.keyword", "displayName": "Domain"}
        ],
        "filters": [
            {"field": "container.product_type.keyword", "selections": ["View"]}
        ],
        "offset": 0,
        "size": 16,
        "sort": "_score:desc",
        "source": ["assetType", "assetId", "uuid", "assetDescription", "tags", "governance.step"],
        "userEmail": user_email
    }

    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code == 200:
        print("Data fetched successfully")
        return response.json()
    else:
        print(f"Failed to fetch data: {response.status_code}")
        print(response.text)
        return None

 
def save_data_to_csv(data, file_path):
    if data:
       
        results = data.get('results', [])
        df = pd.DataFrame(results)
        df.to_csv(file_path, index=False)
        print(f"Data saved to {file_path}")
    else:
        print("No data to save")

if __name__ == "__main__":
 
    tokens_url = "https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    
    
    client_id = " 3"
    client_secret = "28Y8Q2"
    scope = "https://graph.microsoft.com/.default"
    
    
    api_url = "url"
    
  
    search_key = "claims"
    
   
    user_email = "email"
    
     
    file_path = "search_results.csv"
    
    
    access_token = get_access_token(tokens_url, client_id, client_secret, scope)
    
    if access_token:
       
        api_data = get_data_from_search_api(api_url, access_token, search_key, user_email)
        
      
        save_data_to_csv(api_data, file_path)
