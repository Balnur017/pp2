import pygame
import sys

from racer import Player, Enemy, Coin, Obstacle, NitroStrip, PowerUp
from ui import Button, draw_text, input_name_screen
from persistence import save_score, get_top_scores, load_settings, save_settings


pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 400, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Pro")
clock = pygame.time.Clock()


try:
    crash_sound = pygame.mixer.Sound("crash.wav")
except:
    crash_sound = None


try:
    bg_image = pygame.image.load("AnimatedStreet.png").convert()
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
except:
    bg_image = pygame.Surface((WIDTH, HEIGHT))
    bg_image.fill((100, 100, 100))


current_settings = load_settings()


def game_loop(user_name):
    print("GAME STARTED")

    if current_settings.get("sound", True):
        try:
            pygame.mixer.music.load("music.wav")
            pygame.mixer.music.play(-1)
        except:
            pass

    diff_map = {
        "Easy": 4,
        "Medium": 6,
        "Hard": 8
    }

    base_speed = diff_map.get(current_settings.get("difficulty", "Medium"), 5)

    speed = base_speed
    score = 0
    coins = 0
    distance = 0
    finish_line = 5000

    has_shield = False
    nitro_timer = 0
    oil_timer = 0
    bg_y = 0

    p1 = Player(color=current_settings.get("car_color", "Blue"))
    e1 = Enemy()
    c1 = Coin()
    o1 = Obstacle()
    n1 = NitroStrip()
    shield_item = PowerUp("shield")
    repair_item = PowerUp("repair")

    layer_bottom = pygame.sprite.Group(o1, n1)
    layer_mid = pygame.sprite.Group(c1, shield_item, repair_item)
    layer_top = pygame.sprite.Group(p1, e1)

    running = True

    while running:
        curr_t = pygame.time.get_ticks()

        move_speed = speed

        if curr_t < nitro_timer:
            move_speed += 4

        if curr_t < oil_timer:
            move_speed -= 3

        if move_speed < 1:
            move_speed = 1

        distance += move_speed * 0.1

        bg_y += move_speed
        if bg_y >= HEIGHT:
            bg_y = 0

        SCREEN.blit(bg_image, (0, bg_y))
        SCREEN.blit(bg_image, (0, bg_y - HEIGHT))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for sprite in layer_bottom:
            SCREEN.blit(sprite.image, sprite.rect)
            sprite.move(move_speed)

        for sprite in layer_mid:
            SCREEN.blit(sprite.image, sprite.rect)
            sprite.move(move_speed)

        for sprite in layer_top:
            SCREEN.blit(sprite.image, sprite.rect)

            if sprite == p1:
                sprite.move()
            else:
                if sprite.move(move_speed):
                    score += 1

        if pygame.sprite.collide_rect(p1, o1):
            oil_timer = curr_t + 2000
            o1.reset()

        if pygame.sprite.collide_rect(p1, n1):
            nitro_timer = curr_t + 2000
            n1.reset()

        if pygame.sprite.collide_rect(p1, shield_item):
            has_shield = True
            shield_item.reset()

        if pygame.sprite.collide_rect(p1, repair_item):
            speed = base_speed
            oil_timer = 0
            nitro_timer = 0
            repair_item.reset()

        if pygame.sprite.collide_rect(p1, c1):
            old_coins = coins
            coins += c1.weight

            if coins // 5 > old_coins // 5:
                speed += 1

            c1.reset()

        if pygame.sprite.collide_rect(p1, e1):
            if has_shield:
                has_shield = False
                e1.reset()
            else:
                pygame.mixer.music.stop()

                if current_settings.get("sound", True) and crash_sound:
                    crash_sound.play()

                final_score = coins + score
                save_score(user_name, final_score, distance)
                game_over_screen(user_name, final_score, int(distance))
                running = False

        if distance >= finish_line:
            pygame.mixer.music.stop()
            final_score = coins + score + 100
            save_score(user_name, final_score, distance)
            win_screen(user_name, final_score, int(distance))
            running = False

        if curr_t < oil_timer:
            draw_text(SCREEN, "OIL! SLOW DOWN", 28, WIDTH // 2, HEIGHT // 2, (255, 0, 0))

        if curr_t < nitro_timer:
            draw_text(SCREEN, "NITRO BOOST!", 28, WIDTH // 2, HEIGHT // 2 - 50, (0, 255, 0))

        draw_text(SCREEN, f"Dist: {int(distance)}/{finish_line}", 18, WIDTH // 2, 50, (255, 255, 255))
        draw_text(SCREEN, f"Coins: {coins}", 18, 60, 20, (255, 255, 0))
        draw_text(SCREEN, f"Score: {score}", 18, WIDTH - 60, 20, (255, 255, 255))

        if has_shield:
            draw_text(SCREEN, "SHIELD", 15, WIDTH - 60, 45, (0, 200, 255))

        pygame.display.update()
        clock.tick(60)


def leaderboard_screen():
    btn_back = Button(WIDTH // 2, 530, 150, 50, "BACK")

    while True:
        scores = get_top_scores()

        SCREEN.fill((255, 255, 255))
        draw_text(SCREEN, "TOP 10 SCORES", 36, WIDTH // 2, 50)

        for i, entry in enumerate(scores):
            y_pos = 130 + i * 35
            text = f"{i + 1}. {entry['name'][:8]} - {entry['score']} pts"
            draw_text(SCREEN, text, 20, WIDTH // 2, y_pos)

        btn_back.draw(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_back.is_clicked(event.pos):
                    return

        pygame.display.update()
        clock.tick(60)


def settings_screen():
    btn_diff = Button(WIDTH // 2, 200, 220, 50, f"Diff: {current_settings['difficulty']}")
    btn_color = Button(WIDTH // 2, 270, 220, 50, f"Car: {current_settings['car_color']}")
    btn_sound = Button(
        WIDTH // 2,
        340,
        220,
        50,
        f"Sound: {'ON' if current_settings['sound'] else 'OFF'}"
    )
    btn_back = Button(WIDTH // 2, 450, 150, 50, "BACK")

    while True:
        SCREEN.fill((200, 200, 200))

        draw_text(SCREEN, "SETTINGS", 40, WIDTH // 2, 100)

        btn_diff.draw(SCREEN)
        btn_color.draw(SCREEN)
        btn_sound.draw(SCREEN)
        btn_back.draw(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_diff.is_clicked(event.pos):
                    levels = ["Easy", "Medium", "Hard"]
                    current_settings["difficulty"] = levels[
                        (levels.index(current_settings["difficulty"]) + 1) % len(levels)
                    ]
                    btn_diff.text = f"Diff: {current_settings['difficulty']}"

                elif btn_color.is_clicked(event.pos):
                    colors = ["Blue", "Orange", "Pink"]
                    current_settings["car_color"] = colors[
                        (colors.index(current_settings["car_color"]) + 1) % len(colors)
                    ]
                    btn_color.text = f"Car: {current_settings['car_color']}"

                elif btn_sound.is_clicked(event.pos):
                    current_settings["sound"] = not current_settings["sound"]
                    btn_sound.text = f"Sound: {'ON' if current_settings['sound'] else 'OFF'}"

                elif btn_back.is_clicked(event.pos):
                    save_settings(current_settings)
                    return

        pygame.display.update()
        clock.tick(60)


def game_over_screen(name, score, dist):
    btn_retry = Button(WIDTH // 2, 400, 150, 50, "RETRY")
    btn_menu = Button(WIDTH // 2, 480, 150, 50, "MENU")

    while True:
        SCREEN.fill((100, 0, 0))

        draw_text(SCREEN, "GAME OVER", 45, WIDTH // 2, 150, (255, 255, 255))
        draw_text(SCREEN, f"Score: {score}", 25, WIDTH // 2, 230, (255, 255, 255))
        draw_text(SCREEN, f"Distance: {dist}m", 25, WIDTH // 2, 270, (255, 255, 255))

        btn_retry.draw(SCREEN)
        btn_menu.draw(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_retry.is_clicked(event.pos):
                    game_loop(name)
                    return

                elif btn_menu.is_clicked(event.pos):
                    return

        pygame.display.update()
        clock.tick(60)


def win_screen(name, score, dist):
    btn_retry = Button(WIDTH // 2, 400, 150, 50, "RETRY")
    btn_menu = Button(WIDTH // 2, 480, 150, 50, "MENU")

    while True:
        SCREEN.fill((0, 120, 0))

        draw_text(SCREEN, "YOU WIN!", 50, WIDTH // 2, 150, (255, 255, 255))
        draw_text(SCREEN, f"Score: {score}", 25, WIDTH // 2, 230, (255, 255, 255))
        draw_text(SCREEN, f"Distance: {dist}m", 25, WIDTH // 2, 270, (255, 255, 255))

        btn_retry.draw(SCREEN)
        btn_menu.draw(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_retry.is_clicked(event.pos):
                    game_loop(name)
                    return

                elif btn_menu.is_clicked(event.pos):
                    return

        pygame.display.update()
        clock.tick(60)


def main_menu():
    btn_play = Button(WIDTH // 2, 200, 200, 50, "PLAY")
    btn_lead = Button(WIDTH // 2, 280, 200, 50, "LEADERBOARD")
    btn_settings = Button(WIDTH // 2, 360, 200, 50, "SETTINGS")
    btn_quit = Button(WIDTH // 2, 440, 200, 50, "QUIT")

    while True:
        SCREEN.fill((255, 255, 255))

        draw_text(SCREEN, "RACER PRO", 45, WIDTH // 2, 100)

        btn_play.draw(SCREEN)
        btn_lead.draw(SCREEN)
        btn_settings.draw(SCREEN)
        btn_quit.draw(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_play.is_clicked(event.pos):
                    name = input_name_screen(SCREEN, WIDTH, HEIGHT)
                    game_loop(name)

                elif btn_lead.is_clicked(event.pos):
                    leaderboard_screen()

                elif btn_settings.is_clicked(event.pos):
                    settings_screen()

                elif btn_quit.is_clicked(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main_menu()