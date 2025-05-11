from menu import Menu, Button
from game import Player, Game
from music import MusicPlayer
import pygame

if __name__ == '__main__':
    pygame.font.init()
    pygame.mixer.init()

    clock = pygame.time.Clock()
    fps = 60
    screen = pygame.display.set_mode((900, 750))
    pygame.display.set_caption("Адмирал Черменидзе: Щит прибрежной бухты")
    icon = pygame.image.load("resources/images/icon.png").convert_alpha()
    pygame.display.set_icon(icon)

    playlist = [
        "resources/music/music1.mp3",
        "resources/music/music2.mp3",
        "resources/music/music3.mp3",
        "resources/music/music4.mp3"
    ]

    music_player = MusicPlayer(
        playlist=playlist,
        volume=0.1,
        shuffle=True
    )

    MainMenu = Menu("resources/images/menu.png", screen, True)
    LoreMenu = Menu("resources/images/info.png", screen, False)
    GameMenu = Menu("resources/images/game_field.png", screen, False)

    BtnStart = Button(102, 155, 304, 152,
                      image="resources/images/v_boi.png",
                      click_sound="resources/sounds/tifon.wav",
                      hover_sound="resources/sounds/tik.wav",
                      action=lambda: MainMenu.scene_change(GameMenu)
    )

    BtnInfo = Button(115, 300, 380, 80,
                      image="resources/images/info_btn.png",
                      click_sound="resources/sounds/bells.mp3",
                      hover_sound="resources/sounds/tik.wav",
                      action=lambda: MainMenu.scene_change(LoreMenu)
    )

    BtnExit = Button(110, 400, 320, 90,
                     image="resources/images/exit_btn.png",
                     click_sound="resources/sounds/skrip2.wav",
                     hover_sound="resources/sounds/tik.wav",
                     action=pygame.quit
    )

    BtnBack = Button(50, 650, 100, 100,
                      image="resources/images/back2.png",
                      click_sound="resources/sounds/knock.mp3",
                      hover_sound="resources/sounds/tik.wav",
                      action=lambda: LoreMenu.scene_change(MainMenu)
    )

    BtnBack2 = Button(50, 650, 100, 100,
                     image="resources/images/back2.png",
                     click_sound="resources/sounds/knock.mp3",
                     hover_sound="resources/sounds/tik.wav",
                     action=lambda: GameMenu.scene_change(MainMenu)
    )

    player = Player("resources/images/player.png", 40, 80, 450, 600, 950, 750)
    game = Game(900, 750)
    game.player = player

    MainMenu.add_element(BtnStart)
    MainMenu.add_element(BtnInfo)
    MainMenu.add_element(BtnExit)
    LoreMenu.add_element(BtnBack)
    GameMenu.add_element(BtnBack2)
    GameMenu.add_element(game)

    music_player.play()

    running = True
    while running:
        delta_time = clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            active_menus = [menu for menu in [MainMenu, LoreMenu, GameMenu] if menu.display]
            for menu in active_menus:
                menu.update(event)
            music_player.handle_events(event)

        if GameMenu.display:
            menu.game(delta_time)
        else:
            GameMenu.elements[1].reset()

        LoreMenu.draw()
        MainMenu.draw()
        GameMenu.draw()

        font = pygame.font.Font(None, 36)
        fps_text = font.render(f"{int(clock.get_fps())}", True, (255, 255, 255))
        screen.blit(fps_text, (10, 10))

        pygame.display.update()
