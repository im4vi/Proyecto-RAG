from google import genai

client = genai.Client(api_key="KEY_ID")

for model in client.models.list():
    print(model.name)
