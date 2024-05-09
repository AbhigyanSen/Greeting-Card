'''
# DOES NOT WORK WITH BG-REMOVED IMAGES

from PIL import Image

# Load Images
bg_image = Image.open("images\\BG.jpg")  # Replace with your background image path
dp_image = Image.open("Potraits\\120Image-removebg-preview.png")  # Replace with your dp image path

# Target center coordinates for dp image in bg image
target_x = 159
target_y = 180

# Resize Image dynamically to % wrt Bg_image
bg_width, bg_height = bg_image.size
max_dp_width = int(bg_width * 0.6)  
max_dp_height = int(bg_height * 0.6)

dp_width, dp_height = dp_image.size     # Dimesions of Original Image

# Determine the new size that maintains aspect ratio within the target dimensions
ratio = min(max_dp_width / dp_width, max_dp_height / dp_height)
new_size = (int(dp_width * ratio), int(dp_height * ratio))

dp_resized = dp_image.resize(new_size, resample=Image.BILINEAR)  # Or use NEAREST or BICUBIC

# Get dimensions of resized dp image
dp_resized_width, dp_resized_height = dp_resized.size

# Calculate top-left corner coordinates for placement based on center point (target_x, target_y)
x_left = target_x - dp_resized_width // 2  
y_top = target_y - dp_resized_height // 2  

# Create a new image to hold the final composition
final_image = bg_image.copy()

# Paste the resized dp image onto the background image
final_image.paste(dp_resized, (x_left, y_top))

# Save the final image
final_image.save("final_image.jpg")  # Replace with your desired output filename

print("Overlay complete! Check 'final_image.jpg'")
'''

# ------------------------------------------------------

import pandas as pd

df = pd.read_excel("EmployeeDatabase3.xlsx", engine='openpyxl')

# Get NGS from the user
user_ngs = int(input("Enter the NGS of the employee: "))

# Store the name of the user-entered NGS in a variable named 'Text'
Text = df[df['NGS'] == user_ngs]['NAME'].values[0]
print("Name: ", Text)

# ------------------------------------------------------

event = int(input("Enter: "))

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
  image.save(f"{BG_Step3[:-4]}_with_text2.{BG_Step3[-3:]}")

  print("STEP 3, Name on BG Successful")

# Example usage
BG_Step3 = "Output\\STEP2.png"
# Text = "Alexander Harrison"
font_path = "fonts\MontRoyal.ttf"  # Optional, comment out if not using a custom font

add_text_to_image(BG_Step3, Text, font_path=font_path)
print("Success!!")