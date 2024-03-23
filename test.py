import requests

url = "https://api.vk.com/method/METHOD_NAME"
params = {
    "param1": "value1",
    "param2": "value2",
    "access_token": "cba375d5cba375d5cba375d58ec8b4c28eccba3cba375d5ae5f9b9fdc8758d69a3499bf"
}

response = requests.get(url, params=params)
data = response.json()

# Process the response data as needed
