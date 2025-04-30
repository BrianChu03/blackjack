import pygame
import os 
from guiconstants import CARD_WIDTH, CARD_HEIGHT

#load the card assets
def load_card_image():
    #create a place to store the images 
    card_images = {}
    
    #designate the path to the folder that has the card images
    image_folder = os.path.join("assets", "cards")

    #iterate through all files in the folder
    for filename in os.listdir(image_folder):
        #chekc if the file is a png image (might want to change if we add other images that aren't cards)
        if filename.endswith(".png"):
            #extract the card name from the file
            card_name = filename.split(".")[0]

            #create the full path to the image file
            image_path = os.path.join(image_folder, filename)

            #load the image
            image = pygame.image.load(image_path)

            #scale the image to the match the constants
            scaled_image = pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))

            #store the scaled image in the dictionary
            card_images[card_name] = scaled_image

    return card_images
