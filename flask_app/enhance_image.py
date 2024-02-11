from PIL import Image, ImageEnhance

def upscale_and_crop_to_16_9(image_path, upscale_factor=3):
    # Open the image
    with Image.open(image_path) as img:
        # Upscale the image
        img = img.resize((int(img.width * upscale_factor), int(img.height * upscale_factor)), Image.LANCZOS)
        
        # Calculate the new dimensions for a 16:9 aspect ratio
        width, height = img.size
        aspect_ratio = width / height
        
        desired_aspect = 16 / 9
        # Check if the width needs to be adjusted
        if aspect_ratio < desired_aspect:
            # Calculate new height maintaining aspect ratio of 16:9
            new_height = width / desired_aspect
            top = (height - new_height) / 2
            img = img.crop((0, top, width, top + new_height))
        # Check if the height needs to be adjusted
        elif aspect_ratio > desired_aspect:
            # Calculate new width maintaining aspect ratio of 16:9
            new_width = height * desired_aspect
            left = (width - new_width) / 2
            img = img.crop((left, 0, left + new_width, height))

        # Enhance the image by increasing sharpness
        enhancer = ImageEnhance.Sharpness(img)
        enhanced_img = enhancer.enhance(2.0)  # You can adjust the factor to your liking
        
        # Save the enhanced and cropped image
        enhanced_img.save('upscaled_cropped_16_9_image.png')
    
    print('The image has been upscaled, cropped to 16:9, and enhanced.')

# Replace 'your_image.png' with the path to your image
upscale_and_crop_to_16_9('your_image.png')