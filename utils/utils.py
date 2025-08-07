import base64
import requests
import imghdr
import json
import asyncio
from fastapi import HTTPException, UploadFile
from langchain_core.messages import HumanMessage
from llms.llm import model
from starlette.datastructures import UploadFile as StarletteUploadFile


async def get_base64_and_mime(source) -> tuple[str, str]:

    if isinstance(source, StarletteUploadFile):
        image_bytes = await source.read()
        await source.seek(0)
    elif isinstance(source, str):
        resp = requests.get(source, timeout=10)
        if resp.status_code != 200:
            raise HTTPException(status_code=400, detail=f"The image could not be accessed: {source}")
        image_bytes = resp.content
    else:
        raise HTTPException(status_code=400, detail="Invalid image source (only file or URL allowed)")

    img_type = imghdr.what(None, h=image_bytes) or "jpeg"
    mime_type = f"image/{img_type}"
    return base64.b64encode(image_bytes).decode("utf-8"), mime_type


async def analyze_image(url: str = None, file: UploadFile = None):
    if not url and not file:
        raise HTTPException(status_code=400, detail="Must provide a URL or a file")

    base64_img, mime_type = await get_base64_and_mime(file if file else url)
    return await build_message(base64_img, mime_type)


async def build_message(base64_img: str, mime_type: str) -> dict:

    message = HumanMessage(
        content=[
            {"type": "text", "text": """
You are an assistant that analyzes images.
Return ONLY a valid JSON (no explanations, no ```json).
The exact format must be:
{
  "title": "...",
  "categories": ["...", "...", "..."],
  "description": "Provide a detailed description of the image in 3–5 sentences, mentioning objects, colors, setting, and possible context"
}
            """},
            {"type": "image_url", "image_url": f"data:{mime_type};base64,{base64_img}"}
        ]
    )

    response = await asyncio.to_thread(model.invoke, [message])
    raw_output = response.content.strip()

    try:
        return json.loads(raw_output)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail=f"Invalid model response: {raw_output}")
