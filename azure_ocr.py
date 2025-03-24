import os
import requests

# Get API Key and Endpoint from environment variables
API_KEY = os.getenv("AZURE_OCR_KEY")
ENDPOINT = os.getenv("AZURE_OCR_ENDPOINT")

def read_text_from_image(image_path):
    """Reads text from an image using Azure Computer Vision API"""
    
    if not API_KEY or not ENDPOINT:
        print("Error: API key or endpoint not set. Please configure your environment variables.")
        return
    
    with open(image_path, "rb") as image_file:
        headers = {
            "Ocp-Apim-Subscription-Key": API_KEY,
            "Content-Type": "application/octet-stream"
        }
        response = requests.post(f"{ENDPOINT}/vision/v3.2/ocr", headers=headers, data=image_file)

        if response.status_code == 200:
            result = response.json()
            extracted_text = []
            for region in result.get("regions", []):
                for line in region.get("lines", []):
                    words = [word["text"] for word in line.get("words", [])]
                    extracted_text.append(" ".join(words))
            return "\n".join(extracted_text)
        else:
            return f"Error: {response.status_code}, {response.text}"

# Test OCR with an image
image_path = "sample_image.jpg"  # Change this to the actual image path
extracted_text = read_text_from_image(image_path)

if extracted_text:
    print("Extracted Text:\n", extracted_text)
