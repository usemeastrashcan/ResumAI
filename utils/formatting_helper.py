import os
import base64
import requests
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENIAI_API_KEY")  
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 5 * 1024 * 1024

def validate_image(image_path):
    """Validate the input is an image file"""

    if not any(image_path.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS):
        return ValueError("Only PNG, JPG, and JPEG files are allowed")
    
    if os.path.getsize(image_path) > MAX_FILE_SIZE:
        return ValueError(f"File too large. Max size is {MAX_FILE_SIZE/1024/1024}MB")
    
    try:
        with Image.open(image_path) as img:
            img.verify() 
    except Exception as e:
        return ValueError(f"Invalid image file: {str(e)}")

def analyze_cv_formatting(image_path):
    validate_image(image_path)
    
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-4-turbo",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Analyze this CV's visual formatting only. Provide specific recommendations on: "
                                "1. Layout organization 2. Font choices 3. Color scheme 4. Section spacing "
                                "5. Visual hierarchy 6. Professional appearance. "
                                "DO NOT extract or mention any text content. "
                                "Provide concise bullet points."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }
    
    # Send to OpenAI
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload
    )
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        raise Exception(f"API Error: {response.text}")
