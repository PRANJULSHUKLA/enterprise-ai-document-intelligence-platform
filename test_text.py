from app.llm.gemini import client, MODEL_NAME

print("MODEL =", MODEL_NAME)

response = client.models.generate_content(
    model=MODEL_NAME,
    contents="Say only Hello"
)

print(response.text)