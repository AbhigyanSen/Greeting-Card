from PIL import Image, ImageDraw, ImageFont

# Event Selection
event = int(input("Select 1 for Birthday and 2 for Work Anniversary: "))

# STEP 1
def overlay_transparent(BG_Step1, DP_Image, Output_Step1, target_height_percent=0.6, center_coords=(0,0)):
  bg_image = Image.open(BG_Step1)
  dp_image = Image.open(DP_Image).convert("RGBA")  # Convert to RGBA for alpha channel
  
  if event == 1:
      center_coords=(159, 220)
      target_height_percent=0.7
  else:
      center_coords=(1347, 464)
      target_height_percent=0.5

  # Get background image size
  bg_width, bg_height = bg_image.size

  # Calculate target height for DP image
  target_dp_height = int(bg_height * target_height_percent)

  # Resize DP image maintaining aspect ratio
  dp_width, dp_height = dp_image.size
  aspect_ratio = dp_width / dp_height
  new_dp_width = int(target_dp_height * aspect_ratio)
  dp_image = dp_image.resize((new_dp_width, target_dp_height))

  # Calculate position for centered placement
  x_offset = center_coords[0] - int(new_dp_width / 2)
  y_offset = center_coords[1] - int(target_dp_height / 2)

  # Create a mask from the alpha channel of the DP image
  mask = dp_image.getchannel('A')

  # Paste the resized and centered DP image onto the background image using the mask
  bg_image.paste(dp_image, (x_offset, y_offset), mask=mask)

  # Save the resulting image
  bg_image.save(Output_Step1)

  print("STEP 1, DP on BG Successfull")

# Example usage
if event == 1:
    BG_Step1 = "images\\BDay\\BG.png"
else:
    BG_Step1 = "images\\WDay\\BG.png"
DP_Image = "Potraits\\120Image-removebg-preview.png"
Output_Step1 = "Output\\STEP1.png"

overlay_transparent(BG_Step1, DP_Image, Output_Step1)
print("Overlayed DP image on background image successfully!")

# ----------------------------------------------------------

# STEP 2
def overlay_on_existing(BG_Step2, Event_Path, Output_Step2, coordinates=(0, 0), resize_factor=0.5):
  existing_image = Image.open(BG_Step2).convert("RGBA")  # Convert for alpha channel compatibility
  overlay_image = Image.open(Event_Path).convert("RGBA")
  
  if event == 1:
    # coordinates = (60,5)
    resize_factor = 0.4
  else:
    # coordinates = (200,5) 
    resize_factor = 1.1

  # Get existing image size
  existing_width, existing_height = existing_image.size

  # Resize overlay image proportionally
  overlay_width, overlay_height = overlay_image.size
  new_overlay_width = int(overlay_width * resize_factor)
  new_overlay_height = int(overlay_height * (new_overlay_width / overlay_width))  # Maintain aspect ratio
  overlay_image = overlay_image.resize((new_overlay_width, new_overlay_height))

  # Paste the resized overlay image with specified coordinates and mask
  existing_image.paste(overlay_image, coordinates, mask=overlay_image.getchannel('A'))

  # Save the resulting image
  existing_image.save(Output_Step2)

  print("STEP 2, Event on BG Successfull")

# Example usage
BG_Step2 = "Output\\STEP1.png"
if event == 1:
    Event_Path = "images\\BDay\\OV.png"
    coordinates = (60,5)
else:
    Event_Path = "images\\WDay\\OV.png"
    coordinates = (1120,730) 
Output_Step2 = "Output\\STEP2.png"

overlay_on_existing(BG_Step2, Event_Path, Output_Step2, coordinates)
print("Successfully created final image with overlay!")

# ------------------------------------------------------------

# STEP 3 Pre-Req
import pandas as pd

df = pd.read_excel("EmployeeDatabase3.xlsx", engine='openpyxl')

# Get NGS from the user
user_ngs = int(input("Enter the NGS of the employee: "))

# Store the name of the user-entered NGS in a variable named 'Text'
Text = df[df['NGS'] == user_ngs]['NAME'].values[0]
print("Name: ", Text)

# ------------------------------------------------------

# STEP 3
from PIL import Image, ImageDraw, ImageFont

def add_text_to_image(BG_Step3, Text, font_path=None, font_size=50, text_color=(255, 255, 255)):
  image = Image.open(BG_Step3)
  draw = ImageDraw.Draw(image)
  
  if event == 1:
      font_size = 30
  else:
      font_size = 80

  if font_path:
    font = ImageFont.truetype(font_path, font_size)
  else:
    font = ImageFont.truetype(None, font_size)

  text_width, text_height = draw.textsize(Text, font=font)

  def calculate_text_position(box_coords):
    left, top, right, bottom = box_coords
    x_center = int((left + right) / 2)
    y_center = int((top + bottom) / 2)

    # Adjust y-position based on text baseline if needed (optional)
    # baseline = draw.textsize(text, font=font)[1]
    # y_center = int(y_center - baseline / 2)  # Adjust based on your font's baseline

    return x_center, y_center

  # Set text position based on event
  if event == 1:
    text_position = calculate_text_position((48,321,262,359))
    text_color = (255, 111, 101)
  else:
    text_position = calculate_text_position((960, 1006, 1735, 1131))
    text_color = (96, 125, 167)

  # Draw the text on the image
  draw.text(text_position, Text, fill=text_color, font=font, anchor="mm")  # Center-align text

  # Save the modified image
  image.save(f"{BG_Step3[:-4]}_with_name.{BG_Step3[-3:]}")

  print("STEP 3, Name on BG Successful")

# Example usage
BG_Step3 = "Output\\STEP2.png"
# Text = "Alexander Harrison"
font_path = "fonts\MontRoyal.ttf"  # Optional, comment out if not using a custom font

add_text_to_image(BG_Step3, Text, font_path=font_path)
print("Success!!")