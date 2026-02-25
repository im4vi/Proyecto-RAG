from google import genai

client = genai.Client(api_key="AIzaSyD-ybRWMQ2jBXYILZIbQxcPqcsmhw21PMU")

for model in client.models.list():
    print(model.name)
