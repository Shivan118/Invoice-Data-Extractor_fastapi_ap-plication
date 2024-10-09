import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai

#os.getenv("GOOGLE_API_KEY")
my_api_key = "your_gemini_api_key"

genai.configure(api_key = my_api_key)

# Use the Model from Gemini to generate the response

def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content([input, image[0], prompt])
    return response.text

# Handle the Uploaded Images
def input_image_setup(upload_file):
    # check if the file has been uploaed or not
    if upload_file is not None:
        #Read the file into bytes
        bytes_data = upload_file.getvalue()

        image_part = [

            {

                "mime_type": upload_file.type,
                "data": bytes_data
            }
        ]

        return image_part
    
    else:
        raise FileNotFoundError("No upload file")


## Intialize our streamlit application
st.header("Gemini Application")

input = st.text_area("Input Prompt: ", key = "input")

upload_file = st.file_uploader("Choose an images file to upload", 
                             type = ['jpg', 'png', 'jpeg'])

image = ""

if upload_file is not None:
    image = Image.open(upload_file)
    st.image(image, caption = "Upload image...", use_column_width = True)

submit = st.button("Submit your query")

input_prompt = """
                You are an expert in invoice analysis and interpretation.

                Your task is to examine input images of invoices and provide accurate responses to questions based on the information contained within these documents.

                Please analyze each invoice image carefully and be prepared to answer queries regarding various aspects of the invoices, such as:

                1. Invoice details (e.g., number, date, due date)
                2. Vendor and customer information
                3. Itemized list of products or services
                4. Individual and total costs
                5. Tax calculations
                6. Payment terms and methods

                Ensure your responses are clear, concise, and directly relevant to the questions asked about the invoice images.
                """

if submit:
    image_data = input_image_setup(upload_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("The Response is...")
    st.write(response)