#!/usr/bin/env python3
"""
Script to insert title data from input Excel files into the title.jpeg image
in the ATTACHED_ASSETS folder.
"""

import pandas as pd
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def extract_title_data_from_excel(file_path):
    """
    Extract title data from an Excel file's Title sheet.
    
    Args:
        file_path (str): Path to the Excel file
        
    Returns:
        dict: Dictionary containing title data
    """
    try:
        # Read the Title sheet
        title_df = pd.read_excel(file_path, 'Title', header=None)
        
        # Process the title data
        title_data = {}
        for index, row in title_df.iterrows():
            if len(row) >= 2:
                key = str(row[0]).strip() if pd.notna(row[0]) else None
                value = row[1] if pd.notna(row[1]) else None
                
                if key and key != 'nan':
                    # Clean up the key name
                    clean_key = key.replace('*', '').replace(':', '').strip()
                    title_data[clean_key] = value
        
        return title_data
    except Exception as e:
        print(f"Error reading title data from {file_path}: {e}")
        return {}

def insert_title_into_image(title_data, input_image_path, output_path):
    """
    Insert title data into an image.
    
    Args:
        title_data (dict): Dictionary containing title information
        input_image_path (str): Path to the input image
        output_path (str): Path to save the modified image
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Check if input image exists
        if not os.path.exists(input_image_path):
            print(f"Input image not found: {input_image_path}")
            return False
        
        # Load the image
        image = Image.open(input_image_path)
        
        # Create a drawing context
        draw = ImageDraw.Draw(image)
        
        # Try to load a font, fallback to default if not available
        try:
            # Try to use a better font if available
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            try:
                font = ImageFont.truetype("DejaVuSans.ttf", 40)
            except:
                font = ImageFont.load_default()
        
        # Extract title information from data
        project_name = str(title_data.get("Name of Work ;-", "Project Name Not Available"))
        contract_no = str(title_data.get("Agreement No.", ""))
        work_order_no = str(title_data.get("Reference to work order or Agreement", ""))
        
        # Define text positions and content
        texts = [
            (project_name[:80], (50, 50)),  # Limit text length for better display
            (f"Contract No: {contract_no}", (50, 120)),
            (f"Work Order No: {work_order_no}", (50, 190))
        ]
        
        # Add text to image
        for text, position in texts:
            # Add shadow for better visibility
            draw.text((position[0]+2, position[1]+2), text, fill=(0, 0, 0), font=font)
            # Add main text
            draw.text(position, text, fill=(255, 255, 255), font=font)
        
        # Save the modified image
        image.save(output_path, "JPEG", quality=95)
        
        print(f"Modified image saved to: {output_path}")
        return True
    except Exception as e:
        print(f"Error inserting title into image: {e}")
        return False

def process_all_input_files(input_folder="TEST_INPUT_FILES", assets_folder="ATTACHED_ASSETS"):
    """
    Process all Excel files in the input folder and generate customized title images.
    
    Args:
        input_folder (str): Path to the input folder containing Excel files
        assets_folder (str): Path to the assets folder containing title.jpeg
    """
    input_path = Path(input_folder)
    assets_path = Path(assets_folder)
    
    # Check if input folder exists
    if not input_path.exists():
        print(f"Input folder not found: {input_folder}")
        return
    
    # Check if assets folder exists
    if not assets_path.exists():
        print(f"Assets folder not found: {assets_folder}")
        return
    
    # Check if title.jpeg exists
    input_image_path = assets_path / "title.jpeg"
    if not input_image_path.exists():
        print(f"Base title image not found: {input_image_path}")
        return
    
    # Process each Excel file
    for file_path in input_path.glob('*.xlsx'):
        print(f"\nProcessing: {file_path.name}")
        
        # Extract title data
        title_data = extract_title_data_from_excel(file_path)
        
        if title_data:
            # Generate output filename
            output_filename = f"title_modified_{file_path.stem}.jpeg"
            output_path = assets_path / output_filename
            
            # Insert title into image
            if insert_title_into_image(title_data, input_image_path, output_path):
                print(f"Successfully created: {output_filename}")
            else:
                print(f"Failed to create: {output_filename}")
        else:
            print("  No title data found")

def main():
    """Main function to process input files and generate title images."""
    print("Inserting title data from input Excel files into title.jpeg...")
    print("=" * 60)
    
    # Process all input files
    process_all_input_files()
    
    print("\n" + "=" * 60)
    print("Title image generation process completed!")
    print("Check the ATTACHED_ASSETS folder for the generated images.")

if __name__ == "__main__":
    main()