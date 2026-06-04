from fastapi import FastAPI
import json

app = FastAPI()

def load_data():
    with open("patients.json", "r") as file:
        data = json.load(file)
    return data

@app.get("/")
async def read_root():
    return {"Hello": "Patient Management Application"}

@app.get("/about")
def read_about():
    return {"description": "A fully functional API to manage patients records."}

@app.get("/view")
def read_view():
    data = load_data()
    return data