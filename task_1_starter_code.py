import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, portrait
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader  # <-- KEY CHANGE
from typing import Tuple, List

# --- Configuration ---
INPUT_DIR = "input_images"
OUTPUT_PDF = "output.pdf"
# Use portrait(A4) for standard A4 orientation: (595.28, 841.89) in points
PAGE_SIZE = portrait(A4) 

# --- Image Preprocessing ---

def get_bounding_box_of_visible_area(image: Image.Image) -> Tuple[int, int, int, int]:
    """
    Calculates the minimal bounding box around non-transparent pixels.
    Returns: (left, upper, right, lower)
    """
    if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
        # Get the alpha channel
        alpha = image.getchannel('A')
        bbox = alpha.getbbox()
    else:
        bbox = (0, 0, image.width, image.height)
        
    return bbox if bbox is not None else (0, 0, image.width, image.height)


def preprocess_image(image_path: str) -> Image.Image:
    """
    Opens and crops the image to its visible area, preserving content aspect ratio.

    Args:
        image_path (str): The input path of the image

    Returns:
        Image.Image: The cropped image object.
    """
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Error opening image {image_path}: {e}")
        # Return a 1x1 dummy image on failure
        return Image.new('RGB', (1, 1))

    # Crop to the visible area
    bbox = get_bounding_box_of_visible_area(image)
    cropped_image = image.crop(bbox)
    
    # ReportLab's ImageReader works best with RGB or RGBA/PNG data
    if cropped_image.mode not in ('RGB', 'RGBA', 'P'):
        cropped_image = cropped_image.convert('RGBA')

    return cropped_image


# --- PDF Generation (With Robust ImageReader Fix) ---

def generate_pdf(input_dir: str, output_pdf_path : str, page_size: Tuple[float, float]):
    """
    Generates the PDF using ImageReader for better compatibility.
    
    NOTE: The image placement logic inside the loop below is a SIMPLE sequential layout. 
    You must replace this with your OPTIMAL RECTANGLE PACKING ALGORITHM.
    """
    page_width, page_height = page_size
    c = canvas.Canvas(output_pdf_path, pagesize=page_size)
    
    # 1. Gather all image files
    image_files = sorted([f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    
    if not image_files:
        print(f"No images found in {input_dir}. Generating empty (but valid) PDF.")
        c.drawString(inch, page_height - inch, "No images found.")
        c.save() # CRITICAL: Finalize the file
        return

    print(f"Found {len(image_files)} images. Starting PDF generation.")
    
    # Simple Layout State Variables (Replace these with your packing algorithm's state)
    current_x = inch 
    current_y = page_height - inch
    max_row_height = 0 
    
    for filename in image_files:
        image_path = os.path.join(input_dir, filename)
        
        try:
            # Preprocess the image (returns PIL Image object)
            img = preprocess_image(image_path)
            
            # Use ReportLab's ImageReader to handle the PIL Image object directly (KEY FIX)
            img_reader = ImageReader(img)
            
            # --- START: Simple Placement Logic (REPLACE THIS BLOCK) ---
            
            # Target size: Scale image to max 2 inches wide, preserving aspect ratio
            target_width = 2 * inch
            target_height = img.height * target_width / img.width
            
            # Check if image fits on the current row
            if current_x + target_width > page_width - inch:
                # Move to the next row
                current_y -= (max_row_height + 0.2 * inch)
                current_x = inch
                max_row_height = 0
                
                # Check if we need a new page
                if current_y - target_height < inch:
                    c.showPage()
                    current_x = inch
                    current_y = page_height - inch
                    
            # Draw the image
            c.drawImage(img_reader, current_x, current_y - target_height, 
                        width=target_width, height=target_height)
            
            # Update state variables
            current_x += (target_width + 0.2 * inch)
            max_row_height = max(max_row_height, target_height)
            
            # --- END: Simple Placement Logic ---
            
        except Exception as e:
            print(f"Error processing image {filename}: {e}")

    # CRITICAL: Finalize the PDF file
    c.save()
    print(f"✅ PDF successfully generated at: {output_pdf_path}")
    # No temporary file cleanup needed with ImageReader!


# --- Image Compression (Bonus) ---

def compress_images(input_image_path: str, output_image_path: str, compression_level: int=5) -> str:
    # This function is not used in the core PDF generation but is kept for completeness.
    # It would be used if you decide to compress the *source* images first.
    import shutil
    try:
        image = Image.open(input_image_path)
        if image.format == 'PNG':
            image.save(output_image_path, "PNG", compress_level=compression_level)
        elif image.format in ('JPEG', 'JPG'):
            quality_level = max(1, 95 - compression_level * 10)
            image.convert('RGB').save(output_image_path, "JPEG", quality=quality_level)
        else:
            image.save(output_image_path)
        return output_image_path
        
    except Exception as e:
        print(f"Error compressing image {input_image_path}: {e}")
        shutil.copyfile(input_image_path, output_image_path)
        return output_image_path


# --- Main Execution ---

if __name__ == "__main__":
    if not os.path.exists(INPUT_DIR):
        print(f"Error: Input directory '{INPUT_DIR}' not found. Please run 'sample_data_generation.py' first.")
    else:
        generate_pdf(INPUT_DIR, OUTPUT_PDF, PAGE_SIZE)