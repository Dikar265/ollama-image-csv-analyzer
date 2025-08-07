from fastapi import APIRouter, UploadFile, File
from services.analyze import analyze_image_file

router = APIRouter(
    prefix="/analyze-image",
    tags=["Analyze Image"],
)

@router.post("/", summary="Analyze an uploaded image and return AI-generated JSON results")
async def analyze_image(file: UploadFile = File(...)):
    result = await analyze_image_file(file)
    return result
