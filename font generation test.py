from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import random

def generate_images(output_dir, font_path, chars, img_size=(56, 56), num_images=200):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    font = ImageFont.truetype(font_path, size=12)  # Adjust size as needed
    for char in chars:
        char_dir = os.path.join(output_dir, char)
        os.makedirs(char_dir, exist_ok=True)
        for i in range(num_images):
            img = Image.new('L', img_size, color=0)  # Black background
            draw = ImageDraw.Draw(img)
            draw.text((5, 2), char, font=font, fill=255)  # White text
            
            # Apply random transformations
            img = img.resize(img_size)
            
            # Apply random blur
            blur_radius = random.uniform(0, 2)  # Random blur radius between 0 and 2
            img = img.filter(ImageFilter.GaussianBlur(blur_radius))
            
            # Crop 5 pixels off the left and bottom of the image
            if char == "1":
                img = img.crop((10,0, img_size[0]-26,img_size[1]-33))
            else:
                img = img.crop((5, 0, img_size[0]-30, img_size[1] - 31))
            img = img.resize((28, 28))
            
            # Save image
            img.save(os.path.join(char_dir, f"{char}_{i}.png"))

# Example usage
output_dir = "dataset"
font_path = "C:\\Users\\estal\\Downloads\\nintendo-nes-font.ttf"  # Replace with your font path
chars = "0123456789ABCDEF"
generate_images(output_dir, font_path, chars, num_images=10000)
