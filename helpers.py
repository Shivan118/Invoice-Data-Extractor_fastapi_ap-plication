import json
import os

def get_gemini_response(genai, input_text, image_data, prompt):
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content([input_text, image_data[0], prompt])
    return response.text

    """
    def input_image_setup(upload_file):
        if upload_file is not None:
            bytes_data = upload_file.getvalue()
            image_part = [{
                "mime_type": upload_file.type,
                "data": bytes_data
            }]
            return image_part
        else:
            raise ValueError("No upload file provided.")


    """
def input_image_setup(upload_file):
    if upload_file is not None:
        # Read the file into bytes
        bytes_data = upload_file.file.read()  # Use .file to access the underlying file object
        image_part = [{
            "mime_type": upload_file.content_type,  # Get content type directly
            "data": bytes_data
        }]
        return image_part
    else:
        raise ValueError("No upload file provided.")


    """
    def save_to_json(input_text, response_text):
    data = {
        "input": input_text,
        "response": response_text
    }
    with open('output.json', 'a') as json_file:
        json.dump(data, json_file)
        json_file.write('\n')

    """
def save_to_json(input_text, response_text, filename='output.json'):
    data = {
        "input": input_text,
        "response": response_text
    }
    
    # Check if the file exists
    if os.path.exists(filename):
        # Read existing content
        with open(filename, 'r') as json_file:
            existing_data = json_file.read()
        
        # Append with a semicolon before adding new data
        if existing_data and not existing_data.endswith(';'):
            existing_data += ';'
        
        # Append new data
        new_data = json.dumps(data)
        new_content = existing_data + new_data
    else:
        # If file doesn't exist, create it with the first entry
        new_content = json.dumps(data)
    
    # Write back to the file
    with open(filename, 'w') as json_file:
        json_file.write(new_content)

def validate_input(input_text, image_data):
    if not input_text.strip():
        raise ValueError("Input prompt cannot be empty.")
    if not image_data:
        raise ValueError("No image data available.")
