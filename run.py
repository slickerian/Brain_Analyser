import requests
import json

url = "http://localhost:11434/api/generate"

headers = {
    'Content-Type': 'application/json',
}

conversation_history = []

data = {
    "model": "meditron",

    "stream": False,
    "prompt": "What is cancer in 200 words?"
}

response = requests.post(url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
    response_text = response.text
    data = json.loads(response_text)
    actual_response = data["response"]
    print(actual_response)

else:
    print("Error:", response.status_code, response.text)