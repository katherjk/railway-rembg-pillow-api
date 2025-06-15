from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from rembg import remove
from PIL import Image, ImageOps
from io import BytesIO

app = FastAPI()

@app.post("/remove")
async def remove_background(file: UploadFile = File(...)):
    contents = await file.read()

    # Remove background
    bg_removed = remove(contents)

    # Open image
    image = Image.open(BytesIO(bg_removed)).convert("RGBA")

    # Convert to RGB so Pillow filters work
    image = image.convert("RGB")

    # Enhance lighting
    image = ImageOps.autocontrast(image)

    # Resize using correct resampling method
    image.thumbnail((1000, 1000), Image.Resampling.LANCZOS)

    # Save to buffer
    output_buffer = BytesIO()
    image.save(output_buffer, format="PNG")
    output_buffer.seek(0)

    return StreamingResponse(output_buffer, media_type="image/png")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
