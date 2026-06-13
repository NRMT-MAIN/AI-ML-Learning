from fastapi import FastAPI, Path, HTTPException, Query
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

@app.get("/view/{patient_id}")
def view_patient(patient_id : str = Path(..., description="The ID of the patient to retrieve", example="P001")):
    # Path parameter is used to capture the patient_id from the URL and pass it to the function. 
    # ... means that the parameter is required and must be provided in the URL.
    # The description parameter provides additional information about the path parameter for documentation purposes.
    # load all the pateints
    data = load_data()
    # filter the patient with the given id
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description="The field to sort patients by height, weight, bmi")
    , order : str = Query("asc", description="The order to sort patients (asc or desc)")):
    # in order ... this means that order is optional and if not provided, it will default to "asc". 
    
    valid_sort_fields = ["height", "weight", "bmi"]
    if sort_by not in valid_sort_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field. Must be one of {valid_sort_fields}")
    
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order. Must be 'asc' or 'desc'")
    
    data = load_data()
    sorted_data = sorted(data.values(), key=lambda x: x[sort_by], reverse=(order == "desc"))
    return sorted_data