import pygame
import Hero
import Renderer


def main():
    # Initializes pygame module
    pygame.init()

    # Sets base dimensions for game_display
    display_width = 240
    display_height = 192
    size_multiplier = 4
    fps_cap = 20

    # Initializes game_display, clock, and font
    game_display = pygame.display.set_mode((display_width * size_multiplier, display_height * size_multiplier))
    pygame.display.update()
    clock = pygame.time.Clock()
    large_font = pygame.font.Font("Sprites/Minimalist Fonts/Minimal5x7.ttf", 14)
    small_font = pygame.font.Font("Sprites/Minimalist Fonts/Minimal3x5.ttf", 7)

    # Creates hero and renders map
    renderer = Renderer.Renderer("Maps/Town_1.tmx")
    hero = Hero.Hero("hero_name", (14*16, 20*16))  # Temporary spawn point
    battle = None
    in_combat = False

    while True:
        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if in_combat is False:
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    hero.handle_user_input(event)
            else:
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    battle.handle_user_input(event)

        if in_combat is False:
            # Clear surface
            game_display.fill((0, 0, 0))
            # Tuple with hero image, location, and map name is retrieved
            hero_image, hero_loc, map_name, battle = hero.get_info(renderer.tile_grid)

            # If hero activates load point
            if map_name:
                renderer = Renderer.Renderer(map_name)
            # If hero encounters an enemy
            if battle:
                in_combat = True

            # Hero info is passed to renderer and returns a tuple with the surface and camera_offset
            surface, camera_offset = renderer.display_map(hero_image, hero_loc, size_multiplier)

        else:
            surface = battle.display_battle(large_font, small_font, display_width, display_height)
            camera_offset = ((display_width / 6) * size_multiplier, (display_height / 6) * size_multiplier)
            # Checks if battle is over
            if battle.in_combat is False:
                in_combat = False
                battle = None
                hero.action_queue = []

        # Surface is scaled to and blitted to game_display
        surface = pygame.transform.scale(surface, (surface.get_width() * size_multiplier,
                                                   surface.get_height() * size_multiplier))
        game_display.blit(surface, camera_offset)
        # Display FPS in game_display caption
        pygame.display.set_caption(str(int(round(clock.get_fps(), 0))) + " FPS")
        # Update game_display
        pygame.display.update()
        clock.tick(fps_cap)


if __name__ == "__main__":
    main()
