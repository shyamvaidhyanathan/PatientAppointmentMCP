# 🏥 Patient Health Classification Agent

This project demonstrates how to use **FastAPI**, **Model Context Protocol (MCP)**, and **CrewAI** to classify a patient’s health status based on their number of appointments in the past year. The system includes:

- A REST API for patient classification
- An MCP server exposing the API as a callable tool. The tools available in this MCP Server can be listed.
- An CrewAI Agent that invokes the tool given to it using the MCP Server to classify a patient.



---


## 📁 Project Structure

patient_classifier_agent_project/ <br>
├── agent/ <br>
│ └── crewai_agent.py # ADK Agent using CrewAI <br>
├── api/ <br>
│ └── patient_classifier_api.py # FastAPI classification endpoint<br>
├── mcp/<br>
│ └── mcp_server.py # MCP server wrapping the API<br>
├── tools/<br>
│ └── classify_tool.py # Tool wrapper to interface API with agent<br>
├── data/<br>
│ └── appointment_db.py # Dummy appointment data<br>
├── requirements.txt # Python dependencies<br>
└── README.md # This file<br>
<br>
<br>


---

## ⚙️ Setup Instructions

git clone https://github.com/shyamvaidhyanathan/patient-health-agent.git
cd patient-health-agent



### Create a python virtual environment
python -m venv env
source env/bin/activate   # On Windows: env\Scripts\activate

### Install Dependencies
pip install -r requirements.txt



## ⚙️ Execution  Instructions

### Running the Patient Classifier API found inside api directory
python api/main.py


### Running the MCP Server  
uvicorn mcp.mcp_server:app --reload --port 8001


### Running the Agent 
python agent/crewai_agent.py




## 🧠 Health Classification Logic
The patient is classified based on the number of appointments in the past year:

CHRONIC: More than 10 appointments

MODERATE: 5 to 10 appointments

HEALTHY: Less than 5 appointments



## 🛠️ Tech Stack
FastAPI – for building REST API

CrewAI – for autonomous agent management

LangChain – for tool abstraction

Model Context Protocol (MCP) – for wrapping APIs as tools

Uvicorn – for serving ASGI apps



## 📄 License
MIT License


## 🙋‍♀️ Maintainer
Shyam Vaidhyanathan