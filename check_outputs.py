
import os
from dotenv import load_dotenv
from langsmith import Client

load_dotenv()
client = Client()

dataset_name = "ds-granular-oleo-34"
examples = list(client.list_examples(dataset_name=dataset_name))

if examples:
    ex = examples[0]
    print("Inputs keys:", list(ex.inputs.keys()))
    print("Outputs:", ex.outputs)
else:
    print("No examples")
