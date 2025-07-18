# patient_classifier_api.py
###############################################################################
#
#          PoC for CrewAI Agent that invokes a MCP Server 
#          which has a tool to classify a patient.
#
#          The Agent first discovers the tools available in the MCP server
#          and then uses the Classify Patient tool to classify the patient.
#
#          This code is part of a larger project and is intended for demo 
#          purposes only. This code implements a actual API written in FastAPI.
#
#          It uses some dummy data to simulate a patient classification system.
#
###############################################################################


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
from fastapi_mcp import FastApiMCP

app = FastAPI()

# Dummy appointment data store in lieu of a database
# In a real application, this would be replaced with a database query.
appointments_db = [
    {"patient_id": "001", "date": "2024-07-15"},
    {"patient_id": "001", "date": "2024-10-22"},
    {"patient_id": "001", "date": "2025-01-10"},
    {"patient_id": "001", "date": "2025-04-05"},
    {"patient_id": "001", "date": "2025-07-01"},
    {"patient_id": "001", "date": "2025-07-02"},
    {"patient_id": "001", "date": "2025-07-03"},
    {"patient_id": "001", "date": "2025-07-04"},
    {"patient_id": "001", "date": "2025-07-05"},
    {"patient_id": "001", "date": "2025-07-06"},
    {"patient_id": "001", "date": "2025-07-06"},
    {"patient_id": "001", "date": "2025-07-07"},
    {"patient_id": "001", "date": "2025-07-08"},
    {"patient_id": "002", "date": "2025-05-16"},
    {"patient_id": "002", "date": "2025-06-17"},
    {"patient_id": "002", "date": "2025-07-02"},
    {"patient_id": "002", "date": "2025-07-03"},
    {"patient_id": "002", "date": "2025-07-04"},
    {"patient_id": "003", "date": "2025-06-15"},
]


class ClassificationResponse(BaseModel):
    classification: str
    total_appointments_count: int

@app.get("/classify/{patient_id}", response_model=ClassificationResponse, operation_id="Classify Patient")
def classify_patient(patient_id:str):
    appointment_count =0
    today = datetime.today()
    one_year_ago = today - timedelta(days=365)
    
    appointments = [
        a["date"]
        for a in appointments_db
        if a["patient_id"] == patient_id and datetime.strptime(a["date"], "%Y-%m-%d") >= one_year_ago
    ]
    
    appointment_count = len(appointments)
    if appointment_count == 0 or appointment_count is None:
        raise HTTPException(status_code=404, detail="No appointments found in the last year.")
        
    if appointment_count > 10:
        classification = "CHRONIC"
    elif 5 <= appointment_count <= 10:
        classification = "MODERATE"
    else:
        classification = "HEALTHY"

    return ClassificationResponse(classification=classification, total_appointments_count=appointment_count)





# the main block to run the FastAPI application
# This is where the MCP server is mounted and the application starts.
def main():
    mcp = FastApiMCP(app , include_operations=["Classify Patient"])
    mcp.mount()
    import uvicorn
    uvicorn.run("main:app", port=8000, reload=True)

if __name__ == "__main__":
    main()