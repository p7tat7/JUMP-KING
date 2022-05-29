import pygame

import os

import setting
import king
import map_setting
import global_var
import start_menu
import main_menu


def main():

    # Init
    pygame.init()

    clock = pygame.time.Clock()
    pygame.event.set_allowed([pygame.K_a, pygame.K_d, pygame.K_SPACE, pygame.QUIT])
    pygame.display.set_caption(global_var.GAME_TITLE)

    # Create Screen
    game_screen = pygame.display.set_mode(setting.screen_size)
    game_screen.set_alpha(None)

    # Start Menu
    press_start = start_menu.PressStart()
    logo = start_menu.Logo()
    logo_group = pygame.sprite.Group()
    logo_group.add(logo)
    start_menu_start = True
    pygame.mixer.init()
    pygame.mixer.music.set_volume(setting.default_volume)
    pygame.mixer.music.load(setting.background_music1_path)
    pygame.mixer.music.play()
    while start_menu_start:
        clock.tick(setting.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN and logo.completed:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.Sound.play(press_start.click_sound)
                    press_start.clicked = True
        game_screen.fill((0, 0, 0))
        logo_group.update()
        logo_group.draw(game_screen)
        # game_screen.blit(logo.image, logo.rect)
        if logo.completed:
            press_start.update()
            if press_start.show:
                game_screen.blit(press_start.image, press_start.rect)
        if press_start.complete:
            start_menu_start = False

        pygame.display.flip()

    press_start.kill()

    # Main Menu
    positions, menu_box, arrow, arrow_group = main_menu_screen(game_screen)
    main_menu_enter = True
    settings_enter = False
    load_save = False
    box_group = pygame.sprite.Group()
    box_group.add(menu_box)
    select_sound = pygame.mixer.Sound(setting.select_path)
    # game_screen.fill((0, 0, 0))
    while main_menu_enter:
        clock.tick(setting.FPS)
        if not settings_enter:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        arrow.move(1)
                    if event.key == pygame.K_UP:
                        arrow.move(-1)
                    if event.key == pygame.K_RETURN:
                        select_sound.play()
                        action = option_action(setting.options[arrow.index - 1])
                        if action == 2:
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load(setting.opening_music_path)
                            pygame.mixer.music.play()
                            # New game
                            load_save = False
                            logo.fade_in = False
                            logo.fade_out = True
                            menu_box.kill()
                            game_screen.fill((0, 0, 0))
                            pygame.display.flip()
                            welcome_screen(clock, game_screen, logo_group)
                            pygame.mixer.music.stop()
                            main_menu_enter = False
                            settings_enter = False
                            break
                        elif action == 3:
                            settings_enter = True
            # game_screen.fill((0, 0, 0))
            if main_menu_enter:
                box_group.draw(game_screen)
                main_menu_update(game_screen, menu_box, positions, arrow, arrow_group)

                game_screen.blit(logo.image, logo.rect)

        # Setting page

        pygame.display.flip()


    pygame.mixer.music.stop()
    logo.kill()

    # Create Character
    if not load_save:
        king_player = king.MainCharacter(setting.default_xy[0], setting.default_xy[1], setting.character_size, setting.maximum_height, setting.walking_speed)
        global_var.stage_map = map_setting.Map(global_var.stage_no)
        king_player.init_location()

    # Create Environment


    # environment_objects = pygame.sprite.Group()
    player = pygame.sprite.Group()
    # environment_objects.add(king_player)
    player.add(king_player)

    game_started = True

    while game_started:
        clock.tick(setting.FPS)

        # Close Window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


        # Update
        player.update()


        # Background
        backdropbox = game_screen.get_rect()

        game_screen.blit(global_var.background, backdropbox)
        game_screen.blit(global_var.backdrop, backdropbox)
        player.draw(game_screen)
        game_screen.blit(global_var.foreground, backdropbox)

        pygame.display.flip()

    # End
    pygame.quit()


def update_map():
    global_var.background = pygame.image.load(os.path.join(setting.background_path, f"bg{global_var.stage_no}.png"))
    global_var.background = pygame.transform.scale(global_var.background, setting.screen_size)
    global_var.backdrop = pygame.image.load(os.path.join(setting.stage_images_path, f"{global_var.stage_no}.png"))
    global_var.foreground = pygame.image.load(os.path.join(setting.foreground_path, f"fg{global_var.stage_no}.png"))
    global_var.foreground = pygame.transform.scale(global_var.foreground, setting.screen_size)


def main_menu_screen(screen):
    screen.fill((0, 0, 0))
    menu_box1 = main_menu.Box(setting.main_menu_box_xy[0], setting.main_menu_box_xy[1], setting.main_menu_box_size)
    screen.blit(menu_box1.image, menu_box1.rect)
    # pygame.draw.rect(screen, (255, 0, 0), menu_box1.rect, 1)
    size = menu_box1.image.get_size()

    seperate = size[1] // len(setting.options)
    starting_point = menu_box1.rect.y + seperate // 2

    positions = [seperate * option_index + starting_point for option_index in range(len(setting.options))]

    arrow = main_menu.Arrow(menu_box1.rect.x + 50, positions[0], positions)
    arrow_group = pygame.sprite.Group()
    arrow_group.add(arrow)
    # arrow_group.draw(screen)

    return positions, menu_box1, arrow, arrow_group


def main_menu_update(screen, menu_box, positions, arrow, arrow_group):


    arrow_group.draw(screen)

    font = global_var.font1
    for option_index, option in enumerate(setting.options):
        text = font.render(option, True, (255, 255, 255))
        text_rect = text.get_rect(center=(0, positions[option_index]))
        text_rect.x = menu_box.rect.x + 50
        if arrow.index - 1 == option_index:
            text_rect.x += arrow.image.get_size()[0]

        screen.blit(text, text_rect)
    arrow_group.update()


def option_action(option):
    continue_game = setting.option1
    new_game = setting.option2
    settings = setting.option3
    quit_game = setting.option4
    if option == continue_game:
        return 1
    elif option == new_game:
        return 2
    elif option == settings:
        return 3
    elif option == quit_game:
        pygame.quit()


def welcome_screen(clock, screen, logo):
    message = setting.welcome_message
    font = global_var.font1
    logo_alpha = 255
    alpha = 0
    fade_in = True
    fade_out = False
    frame_count = 0
    duration = 9 * setting.FPS
    text_duration = 4 * setting.FPS
    text_count = 0

    while 1:
        screen.fill((0, 0, 0))
        clock.tick(setting.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        logo.update()
        logo_alpha -= 5

        logo.draw(screen)

        text = font.render(message, True, (255, 255, 255))
        text.set_alpha(alpha)
        text_rect = text.get_rect(center=(setting.screen_size[0] // 2, setting.screen_size[1] // 2))
        screen.blit(text, text_rect)

        if logo_alpha < 255 / 2:
            if alpha <= 255 and fade_in:
                alpha += 5
            elif alpha >= 0 and fade_out:
                alpha -= 5

            if alpha >= 255 and fade_in:
                text_count += 1
                if text_count == text_duration:
                    fade_in = False
                    fade_out = True

        frame_count += 1
        if frame_count == duration:
            break
        pygame.display.flip()


if __name__ == '__main__':
    main()

