###############################################################################
#
#          PoC for CrewAI Agent that invokes a MCP Server 
#          which has a tool to classify a patient.
#
#          The Agent first discovers the tools available in the MCP server
#          and then uses the Classify Patient tool to classify the patient.
#
#          This code is part of a larger project and is intended for demo 
#          purposes only. This code implements a custom tool definition.
#
###############################################################################


import requests
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


class classify_patient_tool_inputs(BaseModel):
    """ Input to my custom tool  """
    patient_id:  str = Field(..., description="The ID of the patient to fetch appointments for.")


# This tool is used to classify a patient based on their ID.
    name: str ="Classify Patient"
    description: str ="Classify the patient given patient ID."
    args_schema: type[BaseModel]    = classify_patient_tool_inputs

    def _run(self,patient_id: str) -> list:
        """Classify Patients from the MCP API server."""
        response = requests.get(f"http://127.0.0.1:8000/classify/{patient_id}")
        if response.status_code == 200:
        #    return response.json().get('"classification"', [])
            return response.json()
    
        else:
            return []




