import requests
from django.conf import settings

def check_url_with_google_safe_browsing(url):
    api_url = "https://safebrowsing.googleapis.com/v4/threatMatches:find"
    api_key = settings.GOOGLE_SAFE_BROWSING_API_KEY

    payload = {
        "client": {
            "clientId": "URL Safety Checker", 
            "clientVersion": "1.0.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }

    params = {'key': api_key}
    response = requests.post(api_url, json=payload, params=params)
    print("API Response:", response.status_code, response.json())  # Debug 

    if response.status_code == 200:
        threat_info = response.json()
        if 'matches' in threat_info:
            return True  # URL is unsafe
        else:
            return False  # URL is safe, no matches found
    else:
        return False  # non-200 responses are safe 

