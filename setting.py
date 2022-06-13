import os

# Game Setting
FPS = 30

# Font
font_folder_path = "font"
SourceHanSansCN = os.path.join(font_folder_path, "SourceHanSansCN.otf")
SourceHanSansCN_normal = os.path.join(font_folder_path, "SourceHanSansCN-Normal.otf")

# Screen Settings
screen_size = [1200, 1000]
all_stage_path = "stage_png"
stage_images_path = os.path.join(all_stage_path, "stage")
level_collision_path = os.path.join(all_stage_path, "level")
background_path = os.path.join(all_stage_path, "background")
foreground_path = os.path.join(all_stage_path, "foreground")

# Menu Audio
default_volume = 0.7
audio_path = "audio"
music_path = os.path.join(audio_path, "music")
sfx_path = os.path.join(audio_path, "sfx")

# Menu Text
menu_pic_path = "menu_pic"
logo_path = os.path.join(menu_pic_path, "title_logo.png")
press_space_path = os.path.join(menu_pic_path, "press_space.png")
box_path = os.path.join(menu_pic_path, "box.png")
arrow_path = os.path.join(menu_pic_path, "arrow.png")

# Music
background_music1_path = os.path.join(music_path, "menu_intro.wav")
opening_music_path = os.path.join(music_path, "opening theme.wav")

# SFX
title_hit_path = os.path.join(sfx_path, "title_hit.wav")
press_start_path = os.path.join(sfx_path, "press_start.wav")
menu_open_path = os.path.join(sfx_path, "menu_open.wav")
select_path = os.path.join(sfx_path, "selectA.wav")

# Character Settings
#default_xy = (500, 865)
default_xy = (423, 599)
frame_rate = 100
character_size = [70, 80]
walking_speed = 5
jumping_variable = 200
maximum_secs_for_jump = 1
jumping_px_per_frame = 15
maximum_height = 440
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

# Start Menu
options = ['繼續', '新遊戲', '選項', '退出']
option1 = '繼續'
option2 = '新遊戲'
option3 = '選項'
option4 = '退出'
main_menu_box_xy = (300, 500)
main_menu_box_size = (200, 300)
welcome_message = '傳說頂層有個辣妹 佢叫mingming....'

# Saving
save_data_path = "save_data"

# Game menu
ingame_options = ['繼續', '選項', '保存並退出', '放棄']
ingame_option1 = '繼續'
ingame_option2 = '選項'
ingame_option3 = '保存並退出'
ingame_option4 = '放棄'


