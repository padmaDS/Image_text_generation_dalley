## imports
from openai import OpenAI  # OpenAI Python library to make API calls
import requests  # used to download images
import os  # used to access filepaths
from PIL import Image  # used to print and edit images
from dotenv import load_dotenv
import cv2

from io import BytesIO

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')

## initialize OpenAI client
client = OpenAI(api_key=api_key)

response = client.images.generate(
  model="dall-e-3",
  prompt="""I want to generate a photograph or greeting card for the occasion of 10th Anniversary, with the festival name clearly presented in the image. 
  convey a warm greeting."
  """,
  size="1024x1024",
  quality="standard",
  n=1,
)

image_url = response.data[0].url
# print(image_url)

## Converting the image_url into png or jpeg format

## Download the image
response = requests.get(image_url)
image_data = BytesIO(response.content)

## Open the image with Pillow
image = Image.open(image_data)

## Save the image as PNG
image.save("occasion_image.png", "PNG")

## Save the image as JPG
image = image.convert("RGB")  # Convert to RGB to ensure compatibility with JPG
image.save("occasion_image.jpg", "JPEG")

# ## Changing the Font style and Font Size of the text



# Read the image
img = cv2.imread("occasion_image.png")

# Define the main text and occasional messages
main_lines = [
    "TO THE HEAD OF THE DEPARTMENT.",
    "Arthink,",
    "Mr. Arjun",
    "CEO & CTO"
]

# occasional_messages = [
#     "Occasional Message 1",
#     "Occasional Message 2"
# ]

# Define the "from" address text
from_lines = [
    "From:",
    "The Team at Arthink"
]

# Insert occasional messages at desired positions
# main_lines.insert(1, occasional_messages[0])
# main_lines.insert(4, occasional_messages[1])

# Define the font parameters
font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
font_scale = 1
font_color = (255, 0, 0)
thickness = 2
line_height = 30  # Adjust the line height based on your font and scale

# Define the starting position for the main text
x_main, y_main = 40, 36

# Draw each line of the main text and occasional messages
for i, line in enumerate(main_lines):
    y_position = y_main + i * line_height
    cv2.putText(img, line, (x_main, y_position), font, font_scale, font_color, thickness)

# Calculate the starting position for the "from" address text
y_from = img.shape[0] - (len(from_lines) * line_height) - 36  # 36 pixels from the bottom

# Draw each line of the "from" address text at the bottom right
for i, line in enumerate(from_lines):
    text_size = cv2.getTextSize(line, font, font_scale, thickness)[0]
    x_from = img.shape[1] - text_size[0] - 40  # 40 pixels from the right
    y_position = y_from + i * line_height
    cv2.putText(img, line, (x_from, y_position), font, font_scale, font_color, thickness)

# Save the image with text
cv2.imwrite("output_image_with_text.png", img)

# Display the image using OpenCV's imshow
cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
