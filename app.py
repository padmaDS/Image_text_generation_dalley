from flask import Flask, request, send_file
from openai import OpenAI
import requests
import os
from PIL import Image
import cv2
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)

# Load environment variables
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

@app.route('/engage_bay', methods=['POST'])
def generate_image():
    data = request.json
    prompt = data.get('prompt', '')
    receiver = data.get('receiver', '')
    sender = data.get('sender', '')

    # Generate image from prompt using OpenAI API
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    # Get image URL from OpenAI response
    image_url = response.data[0].url

    # Download and process the image
    response = requests.get(image_url)
    image_data = BytesIO(response.content)
    image = Image.open(image_data)

    # Save image as PNG
    image.save("occasion_image.png", "PNG")

    # Convert image to RGB (required for JPEG)
    image = image.convert("RGB")

    # Save image as JPEG
    image.save("occasion_image.jpg", "JPEG")

    # Load image using OpenCV
    img = cv2.imread("occasion_image.png")

    # Define text parameters
    font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
    font_scale = 1
    font_color = (255, 0, 0)
    thickness = 2
    line_height = 30

    # Calculate text positions
    x_main, y_main = 40, 36
    y_from = img.shape[0] - (len(sender.split('\n')) * line_height) - 36

    # Draw text on the image
    cv2.putText(img, receiver, (x_main, y_main), font, font_scale, font_color, thickness)
    cv2.putText(img, sender, (x_main, y_from), font, font_scale, font_color, thickness)

    # Save the final image
    cv2.imwrite("output_image_with_text.png", img)

    # Return the generated image file
    return send_file("output_image_with_text.png", mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
