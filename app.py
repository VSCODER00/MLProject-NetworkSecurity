import sys
import os

from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.utils import load_object

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline=TrainingPipeline()
        train_pipeline.initiate_training_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise CustomException(e,sys)
    
@app.post("/predict")
async def predict_route(request: Request,file: UploadFile = File(...)):
    try:
        df=pd.read_csv(file.file)
        #print(df)
        preprocessor=load_object("final_model/preprocessor/preprocessor.pkl")
        final_model=load_object("final_model/model.pkl")
        x_transform = preprocessor.transform(df)
        y_pred = final_model.predict(x_transform)
        df['predicted_column'] = y_pred
        df.to_csv('prediction_output/output.csv')
        return {"message": "Prediction successful", "output_file": "prediction_output/output.csv"}


    except Exception as e:
        raise CustomException(e,sys)
    
if __name__=="__main__":
    app_run(app,host="0.0.0.0",port=8000)