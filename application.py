import os
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from helpers import get_gemini_response, input_image_setup, save_to_json, validate_input  # Ensure you have the necessary functions
from fastapi import Request
import google.generativeai as genai

app = FastAPI()

my_api_key = "your_gemini_api_key"

genai.configure(api_key = my_api_key)

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Define a Pydantic model for the input
class InputData(BaseModel):
    input_text: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit/")
async def submit(input_text: str = Form(...), upload_file: UploadFile = File(...)):
    print("Received input:", input_text)  # Check if input_text is received
    image_data = input_image_setup(upload_file)  # Try to set up image
    print("Image data prepared:", image_data)  # Check if image data is set up correctly
    input_prompt = """You are an expert in invoice analysis and interpretation...
                     (Your prompt content here)"""
    try:
        validate_input(input_text, image_data)  # Validate inputs
        print("Inputs validated.")  # Check if validation passes
        
        # Process the request
        response = get_gemini_response(genai, input_text, image_data, input_prompt)
        print("Generated response:", response)  # Check the generated response
        
        # Save the input and response to JSON
        save_to_json(input_text, response)
        
        return {"response": response}
    except ValueError as ve:
        print("ValueError:", str(ve))  # Log ValueError
        return {"error": str(ve)}
    except Exception as e:
        print("Exception:", str(e))  # Log any other exceptions
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
