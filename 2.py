# STEP 1
# from PIL import Image

# def overlay_transparent(bg_image_path, dp_image_path, output_path, target_height_percent=0.6, center_coords=(159, 180)):
#   bg_image = Image.open(bg_image_path)
#   dp_image = Image.open(dp_image_path).convert("RGBA")  # Convert to RGBA for alpha channel

#   # Get background image size
#   bg_width, bg_height = bg_image.size

#   # Calculate target height for DP image
#   target_dp_height = int(bg_height * target_height_percent)

#   # Resize DP image maintaining aspect ratio
#   dp_width, dp_height = dp_image.size
#   aspect_ratio = dp_width / dp_height
#   new_dp_width = int(target_dp_height * aspect_ratio)
#   dp_image = dp_image.resize((new_dp_width, target_dp_height))

#   # Calculate position for centered placement
#   x_offset = center_coords[0] - int(new_dp_width / 2)
#   y_offset = center_coords[1] - int(target_dp_height / 2)

#   # Create a mask from the alpha channel of the DP image
#   mask = dp_image.getchannel('A')

#   # Paste the resized and centered DP image onto the background image using the mask
#   bg_image.paste(dp_image, (x_offset, y_offset), mask=mask)

#   # Save the resulting image
#   bg_image.save(output_path)

#   print("Overlayed and centered DP image on background image successfully!")

# # Example usage
# bg_image_path = "images\\BG.jpg"
# dp_image_path = "Potraits\\120Image-removebg-preview.png"
# output_path = "output_image1.png"

# overlay_transparent(bg_image_path, dp_image_path, output_path)
# print("Overlayed DP image on background image successfully!")

# ----------------------------------------------------------------------------------------

# # STEP 2
# from PIL import Image

# def overlay_on_existing(existing_image_path, overlay_image_path, output_path, coordinates=(0, 0), resize_factor=0.5):
#   existing_image = Image.open(existing_image_path).convert("RGBA")  # Convert for alpha channel compatibility
#   overlay_image = Image.open(overlay_image_path).convert("RGBA")

#   # Get existing image size
#   existing_width, existing_height = existing_image.size

#   # Resize overlay image proportionally
#   overlay_width, overlay_height = overlay_image.size
#   new_overlay_width = int(overlay_width * resize_factor)
#   new_overlay_height = int(overlay_height * (new_overlay_width / overlay_width))  # Maintain aspect ratio
#   overlay_image = overlay_image.resize((new_overlay_width, new_overlay_height))

#   # Paste the resized overlay image with specified coordinates and mask
#   existing_image.paste(overlay_image, coordinates, mask=overlay_image.getchannel('A'))

#   # Save the resulting image
#   existing_image.save(output_path)

#   print("Overlayed and resized image on existing image successfully!")

# # Example usage
# existing_image_path = "output_image1.png"
# # overlay_image_path = "images\\Birth.png"
# overlay_image_path = "images\\WorkAnn.png"
# output_path = "final_output_STEP2.png"
# # coordinates = (50,0)  # BDay
# coordinates = (200,5)  # WAnn

# overlay_on_existing(existing_image_path, overlay_image_path, output_path, coordinates)
# print("Successfully created final image with overlay!")

# ---------------------------------------------------------------------------------

'''
from PIL import Image, ImageDraw, ImageFont

def overlay_with_text(existing_image_path, overlay_image_path, output_path, coordinates=(0, 0), resize_factor=0.3, text="Your Text", font_path="fonts\MontRoyal.ttf", font_size=30, text_color=(255, 255, 255)):
  # Open existing image
  existing_image = Image.open(existing_image_path).convert("RGBA")  # Convert for alpha channel compatibility

  # Overlay image handling (if provided)
  if overlay_image_path:
      overlay_image = Image.open(overlay_image_path).convert("RGBA")

      # Resize overlay image proportionally (if resize_factor provided)
      if resize_factor:
        overlay_width, overlay_height = overlay_image.size
        new_overlay_width = overlay_width * resize_factor  # Fix: multiplication instead of conversion
        new_overlay_height = int(overlay_height * (new_overlay_width / overlay_width))  # Maintain aspect ratio
        overlay_image = overlay_image.resize((new_overlay_width, new_overlay_height))

      # Paste the resized overlay image with specified coordinates and mask
      existing_image.paste(overlay_image, coordinates, mask=overlay_image.getchannel('A'))

  # Get text size
  font = ImageFont.truetype(font_path, font_size)
  text_width, text_height = font.textsize(text)

  # Text placement suggestions (adjust based on your image and preference):
  # Option 1: Centered text at the bottom (common for captions)
  text_x = int((existing_image.width - text_width) / 2)
  text_y = existing_image.height - text_height - 10  # Adjust bottom padding as needed

  # Option 2: Text with some padding from top-left corner
  # text_x = 10  # Adjust left padding
  # text_y = 10  # Adjust top padding

  # Create a Draw object for text rendering
  draw = ImageDraw.Draw(existing_image)

  # Draw the text with specified font, color, and coordinates
  draw.text((text_x, text_y), text, fill=text_color, font=font)

  # Save the resulting image
  existing_image.save(output_path)

  print("Successfully created final image with overlay and text!")

# Example usage (update font path)
existing_image_path = "final_output.png"
overlay_image_path = "images\\Birth.png"  # Uncomment if using an overlay image
output_path = "final_output_with_text.png"
text = "This is my image with text!"

# Update with your actual font path
font_path = "fonts\\MontRoyal.ttf"

font_size = 40
text_color = (0, 0, 255)  # Blue text color

overlay_with_text(existing_image_path, overlay_image_path, output_path, text, font_path, font_size=font_size, text_color=text_color)

print("Successfully created final image with text!")
'''

# ---------------------------------------------------------------

# STEP 3
from PIL import Image, ImageDraw, ImageFont

def add_text_to_image(image_path, text, font_path=None, font_size=30, text_color=(255, 255, 255)):
  # Open the image
  image = Image.open(image_path)

  # Create a drawing object
  draw = ImageDraw.Draw(image)

  # Set font
  if font_path:
      font = ImageFont.truetype(font_path, font_size)
  else:
      font = ImageFont.truetype(None, font_size)

  # Get text dimensions
  text_width, text_height = draw.textsize(text, font=font)

  # Calculate text position (optional, adjust as needed)
  text_position = ((image.width - text_width) // 2, image.height - text_height - 10)

  # Draw the text on the image
  draw.text(text_position, text, fill=text_color, font=font)

  # Save the modified image
  image.save(f"{image_path[:-4]}_with_text.{image_path[-3:]}")  # Add "_with_text" to filename and preserve format

  print(f"Image with text overlay saved as: {image_path[:-4]}_with_text.{image_path[-3:]}")

# Example usage
image_path = "final_output_STEP2.png"
text = "Alexander Harrison"
font_path = "fonts\MontRoyal.ttf"  # Optional, comment out if not using a custom font

add_text_to_image(image_path, text, font_path=font_path)