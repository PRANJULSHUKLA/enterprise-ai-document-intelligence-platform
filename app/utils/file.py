import os
import aiofiles


async def save_to_disk(file:bytes, path:str) -> bool:
    # Ensure the uploads directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)
    # file_path = os.path.join("uploads", filename)
    
    async with aiofiles.open(path, "wb") as out_file:
        content = await file.read()
        await out_file.write(file)
    
    return True
