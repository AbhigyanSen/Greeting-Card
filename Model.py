'''
REQUIREMENTS
pip install diffusers torch accelerate
'''

# IMPORTING LIBRARIES AND MODEL
import pandas as pd
from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler
import torch
from PIL import Image
from PIL import ImageDraw, ImageFont, ImageChops
import cv2

# Loading Stable Diffusion Model
# model_id = "stabilityai/stable-diffusion-2"
# scheduler = EulerDiscreteScheduler.from_pretrained(model_id, subfolder="scheduler")
# pipe = StableDiffusionPipeline.from_pretrained(model_id, scheduler=scheduler, torch_dtype=torch.float16)
# pipe = pipe.to("cuda")

# PROMPT GENERATION
df = pd.read_excel("EmployeeDatabase3.xlsx", engine='openpyxl')

# Function to generate a birthday greeting card based on NGS
def generate_birthday_card(ngs):
    if ngs not in df['NGS'].values:
        return "NGS not found in the database. Please enter a valid NGS."

    employee_data = df[df['NGS'] == ngs].iloc[0]

    greeting_card = (
        f"Create a heartwarming and visually appealing image that captures the essence of "
        f"{employee_data['RITU']} in a {employee_data['TRAVEL']} incorporating {employee_data['COLOUR']} as the background color. "
        f"The image should radiate positivity and excitement."
    )

    return greeting_card

# User-Input Employee ID or NGS
user_ngs = int(input("Enter the NGS of the employee: "))

# Storing the Name of the Employee
Text = df[df['NGS'] == user_ngs]['NAME'].values[0]

# Generate birthday greeting card and store it in the 'prompt' variable
prompt = generate_birthday_card(user_ngs)

# Checking
print(prompt)
print(Text)