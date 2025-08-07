from fastapi import UploadFile
from utils.utils import analyze_image
from fastapi import File, HTTPException
import pandas
import io
from fastapi.responses import JSONResponse
import asyncio

async def analyze_image_file(file: UploadFile = File(None), url: str = None):
    if not file and not url:
        raise HTTPException(status_code=400, detail="You must provide an image file or a URL")

    if file:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Only image files are allowed (jpeg, png, etc.)")

        allowed_types = {
            "image/jpeg",
            "image/png",
            "image/webp",
            "image/gif", 
            "image/bmp", 
            "image/tiff",
            "image/x-icon",
            "image/heic",
            "image/heif",
            "image/svg+xml"
        }
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported image format: {file.content_type}. Allowed: jpeg, png, webp"
            )

    try:
        return await analyze_image(url=url, file=file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



async def analyze_csv_file(file: UploadFile = File(...)):
        
        if not file.filename.lower().endswith(".csv"):
            raise HTTPException(status_code=400, detail="Only CSV files are allowed")

        contents = await file.read()
        df = pandas.read_csv(io.StringIO(contents.decode("utf-8", errors="ignore")))

        if "url" not in df.columns:
            raise HTTPException(status_code=400, detail="The CSV must contain a column called 'URL'")
        tasks = [
            analyze_image(url=str(row["url"]).strip())
            for _, row in df.iterrows() if str(row["url"]).strip()
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        final_results = []
        for url, result in zip(df["url"], results):
            if isinstance(result, Exception):
                final_results.append({"url": url, "error": str(result)})
            else:
                final_results.append(result)

        return JSONResponse(content=final_results)