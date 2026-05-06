import sys
import os
import certifi
import pandas as pd
import pymongo

from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from starlette.responses import RedirectResponse, HTMLResponse
from uvicorn import run as app_run
from fastapi.templating import Jinja2Templates

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.main_utils.utils import load_object
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

# ======================
# ENV SETUP
# ======================
load_dotenv()
mongo_db_url = os.getenv("MONGODB_URL_KEY")

ca = certifi.where()
client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

from networksecurity.constant.training_pipeline import (
    DATA_INGESTION_COLLECTION_NAME,
    DATA_INGESTION_DATABASE_NAME
)

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

# ======================
# FASTAPI APP
# ======================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================
# TEMPLATE (DO NOT MODIFY ENV)
# ======================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# ======================
# ROUTES
# ======================

@app.get("/")
def index():
    return RedirectResponse(url="/docs")


@app.get("/train")
def train():
    try:
        pipeline = TrainingPipeline()
        pipeline.run_pipeline()
        return Response("Training successful")
    except Exception as e:
        raise NetworkSecurityException(e, sys)


@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        # Read data
        df = pd.read_csv(file.file)

        # Load artifacts
        preprocessor = load_object("final_model/preprocessor.pkl")
        model = load_object("final_model/model.pkl")

        network_model = NetworkModel(
            preprocessor=preprocessor,
            model=model
        )

        # Predict
        prediction = network_model.predict(df)
        df["prediction"] = prediction

        # Save output
        os.makedirs("prediction_output", exist_ok=True)
        df.to_csv("prediction_output/output.csv", index=False)

        # Convert to HTML
        table = df.to_html(classes="table table-striped", index=False)

        # SAFE RETURN (NO JINJA CACHE ISSUE)
        return HTMLResponse(content=f"""
        <html>
        <head>
            <title>Prediction Result</title>
        </head>
        <body>
            <h2>Prediction Output</h2>
            {table}
        </body>
        </html>
        """)

    except Exception as e:
        raise NetworkSecurityException(e, sys)


# ======================
# MAIN
# ======================
if __name__ == "__main__":
    app_run(app, host="0.0.0.0", port=8000)