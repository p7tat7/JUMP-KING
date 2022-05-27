import os

# Game Setting
FPS = 30

# Screen Settings
screen_size = [1200, 1000]
all_stage_path = "stage_png"
stage_images_path = os.path.join(all_stage_path, "stage")
level_collision_path = os.path.join(all_stage_path, "level")
background_path = os.path.join(all_stage_path, "background")
foreground_path = os.path.join(all_stage_path, "foreground")

# Character Settings
frame_rate = 100
character_size = [70, 80]
walking_speed = 3
jumping_variable = 300
maximum_secs_for_jump = 0.25
jumping_px_per_frame = 15
maximum_height = 500
character_images_path = "character_png"
character_sound_path = "character_sound"
character_move_ani = os.path.join(character_images_path, 'movement')
character_jump_ani = os.path.join(character_images_path, 'jump')
character_drop_ani = os.path.join(character_images_path, 'drop')
idle_img_name = "stationary.png"
dropping_variable = 1.5 # exponential
dropping_px_per_frame = 2
drop_png_height = 900
drop_png_frame = 60

# Character sound files name
jump_sound = "jump.mp3"
land_sound = "land.mp3"
hit_wall_sound = "hit_wall.mp3"
drop_sound = "drop.mp3"
