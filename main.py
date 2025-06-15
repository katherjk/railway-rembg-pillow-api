from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from rembg import remove
from PIL import Image, ImageOps
from io import BytesIO

app = FastAPI()

@app.post("/remove")
async def remove_background(file: UploadFile = File(...)):
    contents = await file.read()

    # Step 1: Remove background using Rembg
    bg_removed = remove(contents)

    # Step 2: Open the transparent PNG result
    image = Image.open(BytesIO(bg_removed)).convert("RGBA")

    # Step 3: Add a white background behind the transparent image
    bg = Image.new("RGB", image.size, (255, 255, 255))  # white background
    bg.paste(image, mask=image.split()[3])  # use alpha channel as mask

    # Step 4: Optional brightness enhancement
    bg = ImageOps.autocontrast(bg)

    # Step 5: Resize for consistency
    bg.thumbnail((1000, 1000), Image.Resampling.LANCZOS)

    # Step 6: Output to stream
    output_buffer = BytesIO()
    bg.save(output_buffer, format="PNG")
    output_buffer.seek(0)

    return StreamingResponse(output_buffer, media_type="image/png")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
