from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from rembg import remove
from PIL import Image, ImageOps
from io import BytesIO

app = FastAPI()

@app.post("/remove")
async def remove_background(file: UploadFile = File(...)):
    contents = await file.read()
    bg_removed = remove(contents)
    image = Image.open(BytesIO(bg_removed)).convert("RGBA")
    image = ImageOps.autocontrast(image)
    image.thumbnail((1000, 1000), Image.ANTIALIAS)
    output_buffer = BytesIO()
    image.save(output_buffer, format="PNG")
    output_buffer.seek(0)
    return StreamingResponse(output_buffer, media_type="image/png")
