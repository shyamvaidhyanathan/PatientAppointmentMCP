###############################################################################
#
#          PoC for CrewAI Agent that invokes a MCP Server 
#          which has a tool to classify a patient.
#
#          The Agent first discovers the tools available in the MCP server
#          and then uses the Classify Patient tool to classify the patient.
#
###############################################################################
# crewai_agent.py
import sys
import os
# Add the parent directory (project root) to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from crewai import Agent, Task, Crew
from tools.classify_tool import classify_patient_tool  # Ensure this is a BaseTool subclass instance    
classify_patient_tool_instance = classify_patient_tool()
patient_id = ""         #Used Later in the code.

###############   DEFINE THE CREW WITH INPUTS  #####################
def create_crew_with_input(patient_id: str):

    classifier_agent = Agent(
        role="Health Classifier for a Patient",
        goal="Classify a patient using the Classify Patient Tool on a MCP Server given to you.",
        backstory=f"""You are an AI agent and you are given acess to a MCP Server. " \
                   "First discover all the tools available in the MCP server " \
                    "and if there is a tool available to classify a patient "\
                    "then go ahead and classify the patient. """,
        tools=[classify_patient_tool_instance],
        verbose=True
)

    # Task
    classify_task = Task(
            description= "Classify Patient {patient_id}",
            expected_output="Return the classification of {patient_id} ",
            agent=classifier_agent,
            )   

    # Task
    tool_discovery_task = Task(
            description= "Discover all the tools available in this MCP server",
            expected_output="Return the list of tools available in this MCP server.",
            agent=classifier_agent,
            )   

    # Crew with inputs
    return Crew(
        agents=[classifier_agent],
        tasks=[tool_discovery_task,classify_task],  # Placeholder, will be updated later
        verbose=True
    )

if __name__ == "__main__":
    patient_id = input("Enter patient ID : ").strip()
    if patient_id is None:
        print("PatientID cannot be blank. Please try again.")

    crew =create_crew_with_input(patient_id)
    result = crew.kickoff(inputs={"patient_id": patient_id})
    print("Result:", result)