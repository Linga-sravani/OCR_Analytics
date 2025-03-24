import requests
import json
import cv2
import numpy as np
from PIL import Image
import io

# Azure Computer Vision API setup
API_KEY = "12NXAhqrwSg4h4EnmWr6pfvPPbHfnOJgB0e0oHKEsvxhbeoUYdz1JQQJ99BCACYeBjFXJ3w3AAAFACOG37sL"
ENDPOINT = "https://ocr-mac-api.cognitiveservices.azure.com/"

def read_text_from_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            headers = {
                "Ocp-Apim-Subscription-Key": API_KEY,
                "Content-Type": "application/octet-stream"
            }
            response = requests.post(
                f"{ENDPOINT}/vision/v3.2/ocr",
                headers=headers,
                data=image_file.read()
            )

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
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Test OCR with an image
if __name__ == "__main__":
    image_path = "sample_image.jpg"  # Ensure this file exists in the same directory
    text = read_text_from_image(image_path)
    print("Extracted Text:\n", text)