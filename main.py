from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from rembg import remove
from PIL import Image, ImageOps
from io import BytesIO

app = FastAPI()

@app.post("/remove")
async def remove_background(file: UploadFile = File(...)):
    # Step 1: Read uploaded image
    contents = await file.read()

    # Step 2: Remove background
    bg_removed = remove(contents)

    # Step 3: Load image and prepare for enhancement
    image = Image.open(BytesIO(bg_removed)).convert("RGBA")

    # Convert to RGB for compatibility with Pillow filters
    image = image.convert("RGB")

    # Step 4: Auto-enhance image
    image = ImageOps.autocontrast(image)

    # Optional: Resize to reasonable dimensions
    image.thumbnail((1000, 1000), Image.ANTIALIAS)

    # Step 5: Save output to buffer
    output_buffer = BytesIO()
    image.save(output_buffer, format="PNG")
    output_buffer.seek(0)

    return StreamingResponse(output_buffer, media_type="image/png")


# 🔁 Enable local development + Railway compatibility
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
