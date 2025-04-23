from PIL import Image, ImageDraw, ImageFont
import os

def create_test_image(text="Hello, Ollama Vision!", filename="test_image.jpg"):
    """Create a simple test image with text."""
    # Create a new image with white background
    width, height = 800, 600
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    
    # Draw a colored rectangle
    draw.rectangle([(100, 100), (700, 500)], fill="lightblue", outline="blue")
    
    # Add text
    try:
        # Try to use a system font
        font = ImageFont.truetype("Arial", 36)
    except IOError:
        # Fall back to default font
        font = ImageFont.load_default()
    
    draw.text((width//2, height//2), text, fill="black", font=font, anchor="mm")
    
    # Save the image
    image.save(filename)
    print(f"Test image created: {filename}")
    return os.path.abspath(filename)

if __name__ == "__main__":
    filepath = create_test_image()
    print(f"You can use this image to test the vision model: {filepath}")
