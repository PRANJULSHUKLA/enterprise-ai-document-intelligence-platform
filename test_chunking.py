from app.utils.chunker import create_chunks

text = """
Python is an amazing programming language.

""" * 200

chunks = create_chunks(text)

print(len(chunks))

for i, chunk in enumerate(chunks):
    print("=" * 50)
    print(f"Chunk {i}")
    print(chunk[:200])