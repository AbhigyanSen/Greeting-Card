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
model_id = "stabilityai/stable-diffusion-2"
scheduler = EulerDiscreteScheduler.from_pretrained(model_id, subfolder="scheduler")
pipe = StableDiffusionPipeline.from_pretrained(model_id, scheduler=scheduler, torch_dtype=torch.float16)
pipe = pipe.to("cuda")

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

# -------------------------------------------------------------------------------------------

# EVENT MANAGEMENT
Event = int(input("Enter 1 to wish HAPPY BIRTHDAY or 2 to wish HAPPPY WORK ANNIVERSARY: "))
if Event == 1:
  Event = "Happy Birthday"
elif Event == 2:
  Event = "Happy Work Anniversary"
else:
  Event = "Wrong Input"
  
# Checking
print(Event)

# -------------------------------------------------------------------------------------------

# MODEL
num_images = int(input("Enter Number of Images between o and 7: "))
# num_images = 2
# user_ngs = 120

if 0 < num_images <= 6:
    for i in range(num_images):

        # Generate the background image (assuming this part is working correctly)
        image = pipe(prompt).images[0]
        image.save(f"/content/{user_ngs}Image{i+1}.png")

        # Loading the Generating Image and Applying Blur
        GenBackground = cv2.imread(f"{user_ngs}Image{i+1}.png")
        GenBackground = cv2.blur(GenBackground, (10, 10))
        cv2.imwrite(f"{user_ngs}BlurredBgImage{i+1}.png", GenBackground)

        BlurBg = Image.open(f"{user_ngs}BlurredBgImage{i+1}.png")
        Potrait = Image.open(f"Potraits/{user_ngs}Image.jpg")

        # Define the desired size of the circular overlay on BlurBg
        overlay_size = (450, 450)
        resize_ratio = min(overlay_size[0] / Potrait.width, overlay_size[1] / Potrait.height)

        # Resize Potrait accordingly
        new_width = int(Potrait.width * resize_ratio)
        new_height = int(Potrait.height * resize_ratio)
        Potrait_resized = Potrait.resize((new_width, new_height))
        mask = Image.new("L", (new_width, new_height), color=0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, new_width, new_height), fill=255)

        Potrait_cropped = Potrait_resized.copy()
        Potrait_cropped.putalpha(mask)

        # Create a border around the Ellipse
        border_size = 10
        border_color = (0, 0, 0, 0)
        border_image = Image.new("RGBA", (new_width + 2 * border_size, new_height + 2 * border_size), border_color)
        border_image.paste(Potrait_cropped, (border_size, border_size), mask=Potrait_cropped)
        blended_image = ImageChops.multiply(BlurBg.convert("RGBA"), border_image)

        center_x = (BlurBg.width - blended_image.width) // 2
        center_y = (BlurBg.height - blended_image.height) // 2
        BlurBg.paste(blended_image, (center_x, center_y), mask=blended_image)
        BlurBg.save(f"{user_ngs}BlurredBgImage{i+1}.png")
        print("Overlay with blending border completed! Check the output image: merged_image_with_border2.jpg  STEP 1")

        # STEP 2
        # Load the Masked Potrait Image
        MaskPotrait = Image.open(f"Potraits/{user_ngs}Image-removebg-preview.png")

        mask = Image.new("L", MaskPotrait.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, MaskPotrait.width, MaskPotrait.height), fill=255)

        cropped_image = Image.new("RGBA", MaskPotrait.size, (0, 0, 0, 0))
        cropped_image.paste(MaskPotrait, (0, 0), mask=mask)

        cropped_image.save(f"Potraits/{user_ngs}Subject.png")
        print("Image cropped to a circle with transparency! Check the output image: cropped_image_circle2.png   STEP 2")

        # STEP 3
        Foreground = Image.open(f"Potraits/{user_ngs}Subject.png")
        Background = Image.open(f"{user_ngs}BlurredBgImage{i+1}.png")

        Foreground = Foreground.convert("RGBA")
        Background = Background.convert("RGBA")
        width = (Background.width - Foreground.width) // 2
        height = (Background.height - Foreground.height) // 2
        Background.paste(Foreground, (width, height), Foreground)

        # Save this image
        Background.save(f"{user_ngs}Card{i+1}.png", format="png")

        # TEXT
        Card = Image.open(f"{user_ngs}Card{i+1}.png")
        draw = ImageDraw.Draw(Card)

        name_width = int(0.7 * Card.width)
        event_width = int(0.85 * Card.width)

        # Function to find the appropriate font size
        def get_adjusted_font_size(text, target_width):
            font_size = 10  # Initial font size
            while True:
                font = ImageFont.truetype("fonts\\MontRoyal.ttf", font_size)
                text_width, text_height = draw.textsize(text, font=font)
                if text_width >= target_width:
                    break
                font_size += 1
            return font_size

        # Get the first text input and adjust font size accordingly
        # Text = input("Enter Name: ")
        font_size1 = get_adjusted_font_size(Text, name_width)
        font1 = ImageFont.truetype("fonts\\MontRoyal.ttf", font_size1)

        # Get the second text input and adjust font size accordingly
        # Event = input("Enter Event: ")
        font_size2 = get_adjusted_font_size(Event, event_width)
        font2 = ImageFont.truetype("fonts\\MontRoyal.ttf", font_size2)

        # Calculate text dimensions for the first text
        text_width1, text_height1 = draw.textsize(Text, font=font1)

        # Center the first text horizontally
        center_x1 = (Card.width - text_width1) // 2
        text_y1 = 589
        text_width2, text_height2 = draw.textsize(Event, font=font2)
        center_x2 = (Card.width - text_width2) // 2
        text_y2 = 100

        draw.text((center_x1, text_y1), Text, fill=(255, 195, 0), font=font1)
        draw.text((center_x2, text_y2), Event, fill=(49, 49, 255), font=font2)

        # Save the modified image
        Card.save(f"{user_ngs}Card{i+1}.png")
else: 
     print("Please enter a number between 1 and 7.")