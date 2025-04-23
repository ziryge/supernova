"""
Image generation tools for SuperNova AI.
"""

import os
import base64
import requests
from typing import Optional, Dict, Any, List
from ..config.env import DEBUG

# Check for Stable Diffusion API availability
try:
    import stability_sdk
    from stability_sdk import client
    STABILITY_AVAILABLE = True
except ImportError:
    STABILITY_AVAILABLE = False

# Check for OpenAI DALL-E availability
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class ImageGenerator:
    """Image generation tool using available APIs."""

    def __init__(self):
        """Initialize the image generation tool."""
        self.stability_api_key = os.getenv("STABILITY_API_KEY", "")
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.output_dir = os.path.join(os.getcwd(), "output", "images")
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_image(self, prompt: str, style: str = "photorealistic", 
                      aspect_ratio: str = "1:1", num_images: int = 1) -> List[Dict[str, Any]]:
        """
        Generate images based on a text prompt.

        Args:
            prompt: Text description of the desired image
            style: Style of the image (photorealistic, digital art, etc.)
            aspect_ratio: Aspect ratio of the image (1:1, 16:9, etc.)
            num_images: Number of images to generate

        Returns:
            A list of dictionaries containing image information
        """
        # Parse aspect ratio
        width, height = self._parse_aspect_ratio(aspect_ratio)
        
        # Print debug information
        if DEBUG:
            print(f"Generating image with prompt: {prompt}")
            print(f"Style: {style}")
            print(f"Aspect ratio: {aspect_ratio} ({width}x{height})")
            print(f"Number of images: {num_images}")
            print(f"Stability API key available: {bool(self.stability_api_key)}")
            print(f"OpenAI API key available: {bool(self.openai_api_key)}")
            print(f"Stability SDK available: {STABILITY_AVAILABLE}")
            print(f"OpenAI available: {OPENAI_AVAILABLE}")
        
        # Try different image generation methods in order of preference
        if self.stability_api_key and STABILITY_AVAILABLE:
            # If Stability API key is available and package is installed, use Stability
            if DEBUG:
                print("Using Stability AI for image generation")
            return self._stability_generate(prompt, style, width, height, num_images)
        elif self.openai_api_key and OPENAI_AVAILABLE:
            # If OpenAI API key is available and package is installed, use DALL-E
            if DEBUG:
                print("Using OpenAI DALL-E for image generation")
            return self._dalle_generate(prompt, style, width, height, num_images)
        else:
            # Otherwise, use a simulated image generation
            if DEBUG:
                print("Using simulated image generation")
            return self._simulated_generate(prompt, style, width, height, num_images)

    def _parse_aspect_ratio(self, aspect_ratio: str) -> tuple:
        """
        Parse aspect ratio string into width and height.
        
        Args:
            aspect_ratio: Aspect ratio string (e.g., "1:1", "16:9")
            
        Returns:
            Tuple of (width, height)
        """
        # Default to 512x512
        default_size = (512, 512)
        
        try:
            # Parse the aspect ratio
            if ":" in aspect_ratio:
                w_str, h_str = aspect_ratio.split(":")
                w, h = int(w_str), int(h_str)
                
                # Calculate dimensions while maintaining a reasonable size
                base_size = 512
                if w > h:
                    width = base_size
                    height = int(base_size * h / w)
                else:
                    height = base_size
                    width = int(base_size * w / h)
                
                return (width, height)
            else:
                # Handle specific size formats like "512x512"
                if "x" in aspect_ratio:
                    w_str, h_str = aspect_ratio.split("x")
                    return (int(w_str), int(h_str))
        except (ValueError, ZeroDivisionError):
            if DEBUG:
                print(f"Invalid aspect ratio: {aspect_ratio}. Using default size.")
        
        return default_size

    def _stability_generate(self, prompt: str, style: str, width: int, height: int, num_images: int) -> List[Dict[str, Any]]:
        """
        Generate images using Stability AI API.
        
        Args:
            prompt: Text description of the desired image
            style: Style of the image
            width: Image width
            height: Image height
            num_images: Number of images to generate
            
        Returns:
            A list of dictionaries containing image information
        """
        try:
            # Initialize the Stability API client
            stability_api = client.StabilityInference(
                key=self.stability_api_key,
                verbose=DEBUG
            )
            
            # Map style to engine
            engine_id = "stable-diffusion-xl-1024-v1-0"
            if style.lower() == "photorealistic":
                engine_id = "stable-diffusion-xl-1024-v1-0"
            elif style.lower() in ["anime", "cartoon"]:
                engine_id = "stable-diffusion-anime-1"
            
            # Prepare style prompt
            style_prompt = ""
            if style.lower() == "oil painting":
                style_prompt = ", oil painting style"
            elif style.lower() == "watercolor":
                style_prompt = ", watercolor painting style"
            elif style.lower() == "sketch":
                style_prompt = ", pencil sketch style"
            elif style.lower() == "digital art":
                style_prompt = ", digital art style, highly detailed"
            
            # Generate images
            answers = stability_api.generate(
                prompt=f"{prompt}{style_prompt}",
                height=height,
                width=width,
                samples=num_images,
                steps=50
            )
            
            # Process and save the generated images
            results = []
            for i, answer in enumerate(answers):
                # Save the image
                img_path = os.path.join(self.output_dir, f"stability_gen_{i}.png")
                with open(img_path, "wb") as f:
                    f.write(answer.artifacts[0].binary)
                
                # Add to results
                results.append({
                    "path": img_path,
                    "prompt": prompt,
                    "style": style,
                    "width": width,
                    "height": height,
                    "engine": engine_id
                })
            
            return results
        
        except Exception as e:
            if DEBUG:
                print(f"Error using Stability AI API: {e}")
            # Fall back to DALL-E if available
            if self.openai_api_key and OPENAI_AVAILABLE:
                return self._dalle_generate(prompt, style, width, height, num_images)
            else:
                return self._simulated_generate(prompt, style, width, height, num_images)

    def _dalle_generate(self, prompt: str, style: str, width: int, height: int, num_images: int) -> List[Dict[str, Any]]:
        """
        Generate images using OpenAI DALL-E.
        
        Args:
            prompt: Text description of the desired image
            style: Style of the image
            width: Image width
            height: Image height
            num_images: Number of images to generate
            
        Returns:
            A list of dictionaries containing image information
        """
        try:
            # Set OpenAI API key
            openai.api_key = self.openai_api_key
            
            # Prepare style prompt
            style_prompt = ""
            if style.lower() == "oil painting":
                style_prompt = ", oil painting style"
            elif style.lower() == "watercolor":
                style_prompt = ", watercolor painting style"
            elif style.lower() == "sketch":
                style_prompt = ", pencil sketch style"
            elif style.lower() == "digital art":
                style_prompt = ", digital art style, highly detailed"
            elif style.lower() == "anime":
                style_prompt = ", anime style, highly detailed"
            
            # Adjust size for DALL-E (must be one of the supported sizes)
            dalle_size = "1024x1024"  # Default
            if width == height:
                dalle_size = "1024x1024"
            elif width > height:
                dalle_size = "1792x1024"
            else:
                dalle_size = "1024x1792"
            
            # Generate images
            response = openai.Image.create(
                model="dall-e-3",
                prompt=f"{prompt}{style_prompt}",
                size=dalle_size,
                n=min(num_images, 1),  # DALL-E 3 only supports 1 image at a time
                response_format="b64_json"
            )
            
            # Process and save the generated images
            results = []
            for i, image_data in enumerate(response["data"]):
                # Decode the base64 image
                image_bytes = base64.b64decode(image_data["b64_json"])
                
                # Save the image
                img_path = os.path.join(self.output_dir, f"dalle_gen_{i}.png")
                with open(img_path, "wb") as f:
                    f.write(image_bytes)
                
                # Add to results
                results.append({
                    "path": img_path,
                    "prompt": prompt,
                    "style": style,
                    "width": width,
                    "height": height,
                    "engine": "dall-e-3"
                })
            
            return results
        
        except Exception as e:
            if DEBUG:
                print(f"Error using OpenAI DALL-E: {e}")
            return self._simulated_generate(prompt, style, width, height, num_images)

    def _simulated_generate(self, prompt: str, style: str, width: int, height: int, num_images: int) -> List[Dict[str, Any]]:
        """
        Simulate image generation when APIs are not available.
        
        Args:
            prompt: Text description of the desired image
            style: Style of the image
            width: Image width
            height: Image height
            num_images: Number of images to generate
            
        Returns:
            A list of dictionaries containing image information
        """
        # Create placeholder image information
        results = []
        for i in range(num_images):
            results.append({
                "path": None,
                "prompt": prompt,
                "style": style,
                "width": width,
                "height": height,
                "engine": "simulated",
                "message": "Image generation is simulated. No actual image was created."
            })
        
        return results

# Create a singleton instance
image_generator = ImageGenerator()
