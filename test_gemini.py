from app.llm.vision import image_to_markdown

text = image_to_markdown(
    "/mnt/uploads/6a6df1eb5eda86da63547aee/ADHAR.pdf_page_0.jpg"
)

print("=" * 80)
print(text)
print("=" * 80)