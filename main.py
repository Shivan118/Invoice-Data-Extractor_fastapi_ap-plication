import streamlit as st
from PIL import Image
import google.generativeai as genai
from helpers import get_gemini_response, input_image_setup, save_to_json, validate_input    # Import helper functions

my_api_key = "your_gemini_api_key"

genai.configure(api_key = my_api_key)

# Initialize our Streamlit application
st.header("Gemini Application")

input_text = st.text_area("Input Prompt: ", key="input")
upload_file = st.file_uploader("Choose an image file to upload", type=['jpg', 'png', 'jpeg'])

image_data = ""

if upload_file is not None:
    image_data = input_image_setup(upload_file)
    image = Image.open(upload_file)
    st.image(image, caption="Upload image...", use_column_width=True)

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
    try:
        # Validate inputs
        validate_input(input_text, image_data)
        
        # Show loading indicator
        with st.spinner("Processing..."):
            response = get_gemini_response(genai, input_text, image_data, input_prompt)
        
        st.subheader("The Response is...")
        st.write(response)
        
        # Save the input and response to JSON
        save_to_json(input_text, response)

    except ValueError as ve:
        st.error(f"Input Error: {ve}")
    except Exception as e:
        st.error(f"An error occurred: {e}")