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

    # Calculate text positions for receiver
    receiver_lines = receiver.split('\n')
    y_receiver = 36 + len(receiver_lines) * line_height  # Adjust for baseline

    # Calculate text positions for sender
    sender_lines = sender.split('\n')
    y_sender = img.shape[0] - 36 - len(sender_lines) * line_height  # Adjust for bottom alignment

    # Draw text on the image for receiver
    for line in receiver_lines:
        text_size_receiver = cv2.getTextSize(line, font, font_scale, thickness)[0]
        x_receiver = 40
        cv2.putText(img, line, (x_receiver, y_receiver), font, font_scale, font_color, thickness)
        y_receiver += line_height

    # Draw text on the image for sender
    for line in sender_lines:
        text_size_sender = cv2.getTextSize(line, font, font_scale, thickness)[0]
        x_sender = img.shape[1] - text_size_sender[0] - 40  # Adjusted for right alignment
        cv2.putText(img, line, (x_sender, y_sender), font, font_scale, font_color, thickness)
        y_sender += line_height

    # Save the final image
    cv2.imwrite("output_image_with_text.png", img)

    # Return the generated image file
    return send_file("output_image_with_text.png", mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
