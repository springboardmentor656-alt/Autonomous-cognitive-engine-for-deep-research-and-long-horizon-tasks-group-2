# create_experiment.py

import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Import LangSmith client
from langsmith.client import Client

# Get environment variables
API_KEY = os.getenv("LANGSMITH_API_KEY")
PROJECT_NAME = os.getenv("LANGSMITH_PROJECT")

if not API_KEY:
    raise ValueError("LANGSMITH_API_KEY is not set in .env")
if not PROJECT_NAME:
    raise ValueError("LANGSMITH_PROJECT is not set in .env")
    

# Initialize LangSmith client
client = Client(api_key=API_KEY)

# Verify if project exists
projects = client.list_projects()
project_names = [p.name for p in projects]

if PROJECT_NAME not in project_names:
    raise ValueError(f"Project '{PROJECT_NAME}' does not exist. Available projects: {project_names}")

print(f"Using project: {PROJECT_NAME}")

# Create a new experiment
experiment_name = "my_first_experiment"  # Change as needed
experiment = client.create_experiment(
    name=experiment_name,
    project=PROJECT_NAME
)

print(f"Experiment '{experiment_name}' created successfully!")
print("Experiment ID:", experiment.id)
