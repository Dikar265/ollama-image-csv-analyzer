from fastapi import APIRouter, UploadFile, File
from services.analyze import analyze_csv_file

router = APIRouter(
    prefix="/analyze-csv",
    tags=["Analyze CSV"]
)

@router.post("/", summary="Analyze a CSV file containing a 'url' column and return AI-generated JSON results")
async def analyze_csv(file: UploadFile = File(...)):
    return await analyze_csv_file(file)

