import pygame
from player import MusicPlayer
import os

WIDTH, HEIGHT = 520, 340          
WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
GRAY   = (200, 200, 200)
GREEN  = (50,  180,  80)
RED    = (200,  50,  50)
BLUE   = (50,  120, 220)
BG     = (30,   30,  45)
PANEL  = (50,   50,  70)
PROGRESS_BG = (80, 80, 100)
PROGRESS_FG = (0, 200, 100)

def format_time(ms):
    """Преобразует миллисекунды в формат MM:SS"""
    if ms < 0:
        return "00:00"
    seconds = int(ms // 1000)
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

def draw(screen, player, font_big, font_med, font_small):
    screen.fill(BG)

    # Заголовок
    title = font_big.render("Music Player", True, WHITE)
    screen.blit(title, (20, 20))

    # Статус (Playing / Stopped)
    if player.is_playing:
        status_text  = "▶ Now Playing"
        status_color = GREEN
    else:
        status_text  = "⏹ Stopped"
        status_color = RED

    status = font_med.render(status_text, True, status_color)
    screen.blit(status, (20, 70))

    # Панель текущего трека
    pygame.draw.rect(screen, PANEL, (20, 110, WIDTH - 50, 80), border_radius=10)

    track_label = font_small.render("Now playing:", True, GRAY)
    screen.blit(track_label, (35, 120))

    track_name = font_small.render(player.current_track_name(), True, WHITE)
    screen.blit(track_name, (35, 145))

    if player.playlist:
        num = font_small.render(
            f"Track {player.current_index + 1} of {len(player.playlist)}",
            True, GRAY
        )
        screen.blit(num, (35, 165))

    # ==================== ПАНЕЛЬ ВРЕМЕНИ ====================
    y_time = 200

    # Фон прогресс-бара
    pygame.draw.rect(screen, PROGRESS_BG, (30, y_time, WIDTH - 60, 12), border_radius=6)

    if player.is_playing:
        # Текущее время (get_pos возвращает миллисекунды)
        current_ms = pygame.mixer.music.get_pos()
        if current_ms < 0:
            current_ms = 0

        # Общая длительность трека
        try:
            total_ms = player.current_sound.get_length() * 1000 if hasattr(player, 'current_sound') else 0
        except:
            total_ms = 0

        # Прогресс (от 0 до 1)
        progress = current_ms / total_ms if total_ms > 0 else 0
        progress = min(max(progress, 0), 1)

        # Заполненная часть прогресс-бара
        bar_width = int((WIDTH - 60) * progress)
        pygame.draw.rect(screen, PROGRESS_FG, (30, y_time, bar_width, 12), border_radius=6)

        # Время
        elapsed_text = format_time(current_ms)
        total_text   = format_time(total_ms)

        time_str = f"{elapsed_text} / {total_text}"
        time_surf = font_small.render(time_str, True, WHITE)
        screen.blit(time_surf, (WIDTH//2 - time_surf.get_width()//2, y_time + 25))
    else:
        time_surf = font_small.render("00:00 / 00:00", True, GRAY)
        screen.blit(time_surf, (WIDTH//2 - time_surf.get_width()//2, y_time + 25))

    # Управление
    controls = font_small.render(
        "[P] Play   [S] Stop   [N] Next   [B] Back   [Q] Quit",
        True, GRAY
    )
    screen.blit(controls, (20, 290))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Music Player")

    font_big   = pygame.font.SysFont("Arial", 28, bold=True)
    font_med   = pygame.font.SysFont("Arial", 22)
    font_small = pygame.font.SysFont("Arial", 16)

    player = MusicPlayer()
    clock  = pygame.time.Clock()

    # Событие окончания трека
    SONG_END = pygame.USEREVENT + 1
    pygame.mixer.music.set_endevent(SONG_END)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if   event.key == pygame.K_p:  
                    player.play()
                elif event.key == pygame.K_s:  
                    player.stop()
                elif event.key == pygame.K_n:  
                    player.next_track()
                elif event.key == pygame.K_b:  
                    player.previous_track()
                elif event.key == pygame.K_q:  
                    running = False

            if event.type == SONG_END:
                if not getattr(player, 'manual_change', False):
                    player.next_track()
                if hasattr(player, 'manual_change'):
                    player.manual_change = False

        draw(screen, player, font_big, font_med, font_small)
        pygame.display.flip()
        clock.tick(30)

    player.stop()
    pygame.quit()


if __name__ == "__main__":
    main()