import pygame
import os
import guiconstants as c

def load_card_images():
    card_images = {}
    
    image_folder_path = c.CARD_IMAGE_FOLDER

    # Check if the directory exists
    if not os.path.isdir(image_folder_path):
        print(f"Error: Card image directory not found at '{image_folder_path}'.")
        return card_images

    print(f"Loading card images from: {os.path.abspath(image_folder_path)}")

    for filename in os.listdir(image_folder_path):
        if filename.lower().endswith(".png"): # Process only .png files, case-insensitive
            card_name_key = filename[:-4]
            full_image_path = os.path.join(image_folder_path, filename)
            
            print(f"Attempting to load: {full_image_path} with key: {card_name_key}")

            try:
                # Load the image
                image_surface = pygame.image.load(full_image_path)
                
                # Scale the image to the dimensions defined in guiconstants
                scaled_image = pygame.transform.scale(image_surface, (c.CARD_WIDTH, c.CARD_HEIGHT))
                
                # Store the scaled image in the dictionary
                card_images[card_name_key] = scaled_image
                print(f"Successfully loaded and scaled: {filename}")

            except pygame.error as e:
                print(f"Error loading or processing image '{full_image_path}': {e}")
                print("Please ensure the image is a valid format (e.g., PNG) and not corrupted.")
            except AttributeError as e:
                print(f"Error: Missing a required constant (e.g., CARD_WIDTH, CARD_HEIGHT) in guiconstants.py for scaling '{filename}': {e}")
                # Optionally, you could skip scaling if constants are missing, or skip the image.
            except Exception as e:
                # Catch any other unexpected errors during processing of a single file
                print(f"An unexpected error occurred with file '{full_image_path}': {e}")
        else:
            # Optionally print files that are skipped if they aren't PNGs
            # print(f"Skipping non-PNG file: {filename}")
            pass

    if not card_images:
        print(f"No PNG images were successfully loaded from '{image_folder_path}'.")
    else:
        print(f"Finished loading card images. Total images loaded: {len(card_images)}")
        
    return card_images