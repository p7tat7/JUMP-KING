import os

# Game Setting
FPS = 60

# Screen Settings
screen_size = [1200, 1000]
stage_images_path = "stage_png"


# Character Settings
frame_rate = 100
character_size = [70, 80]
walking_speed = 3
jumping_variable = 300
maximum_secs_for_jump = 0.5
jumping_px_per_frame = 10
maximum_height = 500
character_images_path = "character_png"
character_move_ani = os.path.join(character_images_path, 'movement')
character_jump_ani = os.path.join(character_images_path, 'jump')
character_drop_ani = os.path.join(character_images_path, 'drop')
idle_img_name = "stationary.png"
dropping_variable = 1.5 # exponential
dropping_px_per_frame = 2
drop_png_height = 900
drop_png_frame = 60

