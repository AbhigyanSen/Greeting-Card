# IMPORTS ----------------------------------------------------------------------------------------------
import pandas as pd
from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler
import torch
from PIL import Image, ImageDraw, ImageFont, ImageChops
import cv2
import os

# Loading Stable Diffusion Model
model_id = "stabilityai/stable-diffusion-2"
scheduler = EulerDiscreteScheduler.from_pretrained(model_id, subfolder="scheduler")
pipe = StableDiffusionPipeline.from_pretrained(model_id, scheduler=scheduler, torch_dtype=torch.float16)
pipe = pipe.to("cuda")

# PROMPT -----------------------------------------------------------------------------------------------
df = pd.read_excel("/home/dcsadmin/Documents/PersonalisedGreeting/Database/EmployeePreference.xlsx", engine='openpyxl')

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

# Get NGS from the user
user_ngs = int(input("Enter the NGS of the employee: "))

# Store the name of the user-entered NGS in a variable named 'Text'
Text = df[df['NGS'] == user_ngs]['NAME'].values[0]
print(Text)

# Generate birthday greeting card and store it in the 'prompt' variable
prompt = generate_birthday_card(user_ngs)

# Print the generated string or error message
print(prompt)

# EVENT SELECTION --------------------------------------------------------------------------------------
Event = int(input("Enter 1 for Birthday and 2 for Anniversary: "))
if Event == 1:
    Event = "Happy Birthday"
elif Event == 2:
    Event = "Happy Anniversary"
else:
    print("Wrong Event Input! Please Enter 1 or 2")
    exit()
    
# IMAGE GENERATION -------------------------------------------------------------------------------------
num_images = int(input("Enter Number of Images between 0 and 6: "))

if 0 <= num_images <= 6:
    for i in range(num_images):

        # Background Image Generation
        image = pipe(prompt).images[0]
        image.save(f"/home/dcsadmin/Documents/PersonalisedGreeting/GeneratedImages/{user_ngs}Image{i+1}.png")

        # Blur Background Image
        GenBackground = cv2.imread(f"/home/dcsadmin/Documents/PersonalisedGreeting/GeneratedImages/{user_ngs}Image{i+1}.png")
        GenBackground = cv2.blur(GenBackground, (10, 10))
        cv2.imwrite(f"/home/dcsadmin/Documents/PersonalisedGreeting/GeneratedImages/{user_ngs}BlurredBgImage{i+1}.png", GenBackground)

        BlurBg = Image.open(f"/home/dcsadmin/Documents/PersonalisedGreeting/GeneratedImages/{user_ngs}BlurredBgImage{i+1}.png")
        Potrait = Image.open(f"/home/dcsadmin/Documents/PersonalisedGreeting/Potraits/{user_ngs}Image.jpg")

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
        BlurBg.save(f"/home/dcsadmin/Documents/PersonalisedGreeting/GeneratedImages/{user_ngs}BlurredBgImage{i+1}.png")
        print("Overlay with blending border completed! Check the output image: merged_image_with_border2.jpg  STEP 1")

        # STEP 2
        # Load the Masked Potrait Image
        MaskPotrait = Image.open(f"/home/dcsadmin/Documents/PersonalisedGreeting/Potraits/MaskedPotraits/{user_ngs}Image-removebg-preview.png")

        mask = Image.new("L", MaskPotrait.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, MaskPotrait.width, MaskPotrait.height), fill=255)

        cropped_image = Image.new("RGBA", MaskPotrait.size, (0, 0, 0, 0))
        cropped_image.paste(MaskPotrait, (0, 0), mask=mask)

        cropped_image.save(f"/home/dcsadmin/Documents/PersonalisedGreeting/GeneratedImages/Pot{user_ngs}Subject.png")
        print("Image cropped to a circle with transparency! Check the output image: cropped_image_circle2.png   STEP 2")

        # STEP 3
        Foreground = Image.open(f"/home/dcsadmin/Documents/PersonalisedGreeting/GeneratedImages/Pot{user_ngs}Subject.png")
        Background = Image.open(f"/home/dcsadmin/Documents/PersonalisedGreeting/GeneratedImages/{user_ngs}BlurredBgImage{i+1}.png")

        Foreground = Foreground.convert("RGBA")
        Background = Background.convert("RGBA")
        width = (Background.width - Foreground.width) // 2
        height = (Background.height - Foreground.height) // 2
        Background.paste(Foreground, (width, height), Foreground)

        # Save this image
        Background.save(f"/home/dcsadmin/Documents/PersonalisedGreeting/GeneratedImages/{user_ngs}Card{i+1}.png", format="png")

        # TEXT
        # Check if the font file exists
        font_path = "/home/dcsadmin/Documents/PersonalisedGreeting/Fonts/Mont_Royal.ttf"
        if not os.path.isfile(font_path):
            raise FileNotFoundError(f"Font file not found: {font_path}")

        # Function to find the appropriate font size
        def get_adjusted_font_size(text, target_width, draw):
            font_size = 10 
            while True:
                font = ImageFont.truetype(font_path, font_size)
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
                if text_width >= target_width:
                    break
                font_size += 1
            return font_size
        
        Card = Image.open(f"/home/dcsadmin/Documents/PersonalisedGreeting/GeneratedImages/{user_ngs}Card{i+1}.png")
        draw = ImageDraw.Draw(Card)
        
        name_width = int(0.7 * Card.width)
        event_width = int(0.85 * Card.width)
        
        # Get the first text input and adjust font size accordingly
        # Text = input("Enter Name: ")
        font_size1 = get_adjusted_font_size(Text, name_width, draw)
        font1 = ImageFont.truetype(font_path, font_size1)
        
        # Get the second text input and adjust font size accordingly
        # Event = input("Enter Event: ")
        font_size2 = get_adjusted_font_size(Event, event_width, draw)
        font2 = ImageFont.truetype(font_path, font_size2)
        
        # Calculate text dimensions for the first text
        bbox1 = draw.textbbox((0, 0), Text, font=font1)
        text_width1, text_height1 = bbox1[2] - bbox1[0], bbox1[3] - bbox1[1]
        
        # Center the first text horizontally
        center_x1 = (Card.width - text_width1) // 2
        text_y1 = 589
        bbox2 = draw.textbbox((0, 0), Event, font=font2)
        text_width2, text_height2 = bbox2[2] - bbox2[0], bbox2[3] - bbox2[1]
        center_x2 = (Card.width - text_width2) // 2
        text_y2 = 100
        
        draw.text((center_x1, text_y1), Text, fill=(255, 195, 0), font=font1)
        draw.text((center_x2, text_y2), Event, fill=(49, 49, 255), font=font2)
        
        # Save the modified image
        Card.save(f"/home/dcsadmin/Documents/PersonalisedGreeting/GeneratedImages/{user_ngs}Card{i+1}.png")
else:
    print("Please enter a number between 0 and 6.")
    
# CLEANUP ----------------------------------------------------------------------------------------------
# Directory containing the images
image_dir = "/home/dcsadmin/Documents/PersonalisedGreeting/GeneratedImages/"
# Desired images to keep
desired_images = [f"{user_ngs}Card{i+1}.png" for i in range(num_images)]

# Iterate through all files in the directory
for filename in os.listdir(image_dir):
    file_path = os.path.join(image_dir, filename)
    # Check if the current file is in the list of desired images
    if filename not in desired_images:
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")