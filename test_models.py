from app.llm.gemini import client

for model in client.models.list():
    print(model.name)