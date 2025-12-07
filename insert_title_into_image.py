#!/usr/bin/env python3
"""
Script to insert title data into the title.jpeg image in the ATTACHED_ASSETS folder.
This script adds text overlay to the title.jpeg image based on data provided.
"""

import os
from pathlib import Path
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import json

def load_config():
    """
    Load configuration from config/title_config.json
    """
    config_path = os.path.join("config", "title_config.json")
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    else:
        # Return default configuration
        return {
            "title_data": {
                "Project Name": "Smart Building Electrical Works",
                "Contract No": "CB/ELEC/2025/001",
                "Work Order No": "WO/ELEC/2025/045"
            },
            "image_settings": {
                "font_size": 40,
                "text_positions": {
                    "project_name": [50, 50],
                    "contract_no": [50, 120],
                    "work_order_no": [50, 190]
                },
                "text_color": [255, 255, 255],
                "shadow_color": [0, 0, 0],
                "shadow_offset": [2, 2]
            }
        }

def insert_title_into_image(title_data=None, output_path=None):
    """
    Insert title data into the title.jpeg image.
    
    Args:
        title_data (dict): Dictionary containing title information. If None, loads from config.
        output_path (str): Path to save the modified image (optional)
    
    Returns:
        str: Path to the modified image
    """
    # Load config if no title_data provided
    if title_data is None:
        config = load_config()
        title_data = config.get("title_data", {})
        image_settings = config.get("image_settings", {})
    else:
        # Use default image settings when title_data is provided
        image_settings = {
            "font_size": 40,
            "text_positions": {
                "project_name": [50, 50],
                "contract_no": [50, 120],
                "work_order_no": [50, 190]
            },
            "text_color": [255, 255, 255],
            "shadow_color": [0, 0, 0],
            "shadow_offset": [2, 2]
        }
    
    # Define paths
    assets_folder = "ATTACHED_ASSETS"
    input_image = os.path.join(assets_folder, "title.jpeg")
    
    # Check if input image exists
    if not os.path.exists(input_image):
        raise FileNotFoundError(f"Input image not found: {input_image}")
    
    # Load the image
    image = Image.open(input_image)
    
    # Create a drawing context
    draw = ImageDraw.Draw(image)
    
    # Try to load a font, fallback to default if not available
    try:
        # Try to use a better font if available
        font = ImageFont.truetype("arial.ttf", image_settings.get("font_size", 40))
    except:
        try:
            font = ImageFont.truetype("DejaVuSans.ttf", image_settings.get("font_size", 40))
        except:
            font = ImageFont.load_default()
    
    # Extract title information from data
    project_name = title_data.get("Project Name", "Project Name Not Available")
    contract_no = title_data.get("Contract No", "")
    work_order_no = title_data.get("Work Order No", "")
    
    # Get text positions from config
    positions = image_settings.get("text_positions", {})
    project_pos = positions.get("project_name", [50, 50])
    contract_pos = positions.get("contract_no", [50, 120])
    work_order_pos = positions.get("work_order_no", [50, 190])
    
    # Get colors from config
    text_color = tuple(image_settings.get("text_color", [255, 255, 255]))
    shadow_color = tuple(image_settings.get("shadow_color", [0, 0, 0]))
    shadow_offset = image_settings.get("shadow_offset", [2, 2])
    
    # Define text positions and content
    texts = [
        (project_name, project_pos),
        (f"Contract No: {contract_no}", contract_pos),
        (f"Work Order No: {work_order_no}", work_order_pos)
    ]
    
    # Add text to image
    for text, position in texts:
        # Add shadow for better visibility
        shadow_pos = (position[0] + shadow_offset[0], position[1] + shadow_offset[1])
        draw.text(shadow_pos, text, fill=shadow_color, font=font)
        # Add main text
        draw.text(position, text, fill=text_color, font=font)
    
    # Determine output path
    if output_path is None:
        output_path = os.path.join(assets_folder, "title_modified.jpeg")
    
    # Save the modified image
    image.save(output_path, "JPEG", quality=95)
    
    print(f"Modified image saved to: {output_path}")
    return output_path

def load_sample_title_data():
    """
    Load sample title data for testing purposes.
    """
    config = load_config()
    return config.get("title_data", {
        "Project Name": "Smart Building Electrical Works",
        "Contract No": "CB/ELEC/2025/001",
        "Work Order No": "WO/ELEC/2025/045"
    })

def load_title_data_from_excel_file(excel_file_path):
    """
    Load title data from an Excel file's Title sheet.
    
    Args:
        excel_file_path (str): Path to the Excel file
    
    Returns:
        dict: Title data dictionary
    """
    try:
        # Read the Title sheet
        title_df = pd.read_excel(excel_file_path, 'Title', header=None)
        
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
        
        # Map Excel keys to our expected keys
        mapped_data = {}
        key_mapping = {
            'Name of Work ;-': 'Project Name',
            'Reference to work order or Agreement': 'Work Order No',
            'Agreement No.': 'Contract No',
            'TENDER PREMIUM %': 'Tender Premium %'
        }
        
        for excel_key, config_key in key_mapping.items():
            if excel_key in title_data:
                mapped_data[config_key] = title_data[excel_key]
        
        return mapped_data
    except Exception as e:
        print(f"Error loading title data from Excel file: {e}")
        return {}

if __name__ == "__main__":
    import sys
    
    # Example usage
    print("Inserting title data into image...")
    
    # Check if an Excel file path is provided as command line argument
    if len(sys.argv) > 1:
        excel_file_path = sys.argv[1]
        print(f"Loading title data from Excel file: {excel_file_path}")
        title_data = load_title_data_from_excel_file(excel_file_path)
        if not title_data:
            print("Failed to load title data from Excel file, using default config...")
            title_data = load_sample_title_data()
        output_filename = f"title_modified_{Path(excel_file_path).stem}.jpeg"
    else:
        # Load sample data (in a real scenario, this would come from your application data)
        print("Using default configuration...")
        title_data = load_sample_title_data()
        output_filename = "title_modified.jpeg"
    
    try:
        # Insert title into image
        output_file = insert_title_into_image(title_data, output_filename)
        print(f"Success! Modified image saved as: {output_file}")
    except Exception as e:
        print(f"Error: {e}")