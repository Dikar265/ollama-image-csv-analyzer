from fastapi import FastAPI
from routes import analyze_image, analyze_csv
import requests

app = FastAPI()

app.include_router(analyze_image.router)
app.include_router(analyze_csv.router)

