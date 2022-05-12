import os

# Game Setting
FPS = 10

# Screen Settings
screen_size = [1000, 1000]
stage_images_path = "stage_png"



# Character Settings
character_size = [50, 70]
walking_speed = 5
jumping_height = 0
character_images_path = "character_png"
character_move_ani = os.path.join(character_images_path, 'movement')
character_jump_ani = os.path.join(character_images_path, 'jump')
character_drop_ani = os.path.join(character_images_path, 'drop')
idle_img_name = "stationary.png"
