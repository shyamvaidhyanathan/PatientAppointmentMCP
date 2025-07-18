# mcp_server.py
###############################################################################
#
#          PoC for CrewAI Agent that invokes a MCP Server 
#          which has a tool to classify a patient.
#
#          The Agent first discovers the tools available in the MCP server
#          and then uses the Classify Patient tool to classify the patient.
#
#          This code is part of a larger project and is intended for demo 
#          purposes only. This code implements a MCP Server with it's endpoints
#          to discover the tools and run them. 
#
###############################################################################

from fastapi import FastAPI
from langchain.tools import tool

# This is the wrapper FastAPI that exposes MCP
app = FastAPI()

# Define tool logic using langchain
@tool
def classify_patient_tool(patient_id: str) -> str:
    """Classifies a patient as CHRONIC, MODERATE, or HEALTHY """
    import requests
    response = requests.post(
        "http://localhost:8000/classify",  # Make sure your FastAPI is running on this port
        json={"patient_id": patient_id}
    )
    return response.json()

# MCP style tool registry
tools_registry = {
    "classify_patient": classify_patient_tool,
}


#List all the tools available in the MCP server
@app.get("/mcp/tools")
def list_tools():
    return list(tools_registry.keys())


@app.post("/mcp/tools/{tool_name}")
def run_tool(tool_name: str, input: dict):
    if tool_name not in tools_registry:
        return {"error": "Tool not found"}
    return tools_registry[tool_name].run(input["patient_id"])
