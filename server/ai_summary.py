from dotenv import load_dotenv
import os
import json
from mistralai import Mistral
from datetime import datetime
load_dotenv()

api_key = os.environ["API_KEY"]
model = "mistral-large-latest"

client = Mistral(api_key=api_key)

def generate_company_summary(company_data):
    messages = [{
        "role": "user",
        "content": (
            "Generate a detailed summary of the company based on the following data. "
            "The summary should highlight key aspects such as the company's strengths, weaknesses, "
            "market position, and any other notable features. "
            "Return a JSON object with a 'summary' key containing the generated summary. "
            f"Company Data: {json.dumps(company_data)}"
        )
    }]
    
    response = client.chat.complete(
        model=model,
        messages=messages,
        response_format={"type": "json_object"}
    )
    
    summary_response = json.loads(response.choices[0].message.content)
    return summary_response
