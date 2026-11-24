from pathlib import Path

import pygame


class MusicPlayer:
    """Here is a keyboard-controlled music player with a playlist."""

    WIDTH = 760
    HEIGHT = 440

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Keyboard Music Player")
        self.timer = pygame.time.Clock()

        self.title_font = pygame.font.Font(None, 48)
        self.text_font = pygame.font.Font(None, 30)
        self.small_font = pygame.font.Font(None, 24)

        music_folder = Path(__file__).parent / "music" / "sample_tracks"
        self.playlist = sorted(music_folder.glob("*.wav"))
        if not self.playlist:
            raise FileNotFoundError("No WAV files were found in music/sample_tracks")

        self.current_index = 0
        self.is_playing = False
        self.started_at = 0
        self.paused_position = 0

    @property
    def current_track(self):
        """Here is the currently selected track."""
        return self.playlist[self.current_index]

    def play(self):
        """Here is the method that starts the selected track."""
        pygame.mixer.music.load(self.current_track)
        pygame.mixer.music.play()
        self.is_playing = True
        self.started_at = pygame.time.get_ticks()
        self.paused_position = 0

    def stop(self):
        """Here is the method that stops playback."""
        pygame.mixer.music.stop()
        self.is_playing = False
        self.paused_position = 0

    def next_track(self):
        """Here is the method that selects and plays the next track."""
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play()

    def previous_track(self):
        """Here is the method that selects and plays the previous track."""
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play()

    def get_position(self):
        """Here is the playback position in seconds."""
        if not self.is_playing:
            return 0
        position_ms = pygame.mixer.music.get_pos()
        return max(0, position_ms) / 1000

    def draw(self):
        """Here is the music player interface."""
        self.screen.fill((20, 25, 38))

        title = self.title_font.render("Music Player", True, (240, 244, 255))
        self.screen.blit(title, title.get_rect(center=(self.WIDTH // 2, 58)))

        track_name = self.current_track.stem.replace("_", " ").title()
        track_text = self.text_font.render("Current track: " + track_name, True, (104, 220, 190))
        self.screen.blit(track_text, track_text.get_rect(center=(self.WIDTH // 2, 135)))

        status = "PLAYING" if self.is_playing and pygame.mixer.music.get_busy() else "STOPPED"
        status_text = self.text_font.render("Status: " + status, True, (255, 205, 90))
        self.screen.blit(status_text, status_text.get_rect(center=(self.WIDTH // 2, 180)))

        position = self.get_position()
        position_text = self.text_font.render(f"Position: {position:05.1f} seconds", True, (220, 225, 235))
        self.screen.blit(position_text, position_text.get_rect(center=(self.WIDTH // 2, 225)))

        # Here is a repeating progress bar for the included five-second samples.
        progress = min(position / 5.0, 1.0)
        bar_rect = pygame.Rect(130, 260, 500, 22)
        pygame.draw.rect(self.screen, (65, 72, 88), bar_rect, border_radius=10)
        fill_rect = pygame.Rect(bar_rect.x, bar_rect.y, int(bar_rect.width * progress), bar_rect.height)
        pygame.draw.rect(self.screen, (104, 220, 190), fill_rect, border_radius=10)

        controls = "P = Play    S = Stop    N = Next    B = Back    Q = Quit"
        controls_text = self.small_font.render(controls, True, (220, 225, 235))
        self.screen.blit(controls_text, controls_text.get_rect(center=(self.WIDTH // 2, 345)))

        playlist_text = f"Track {self.current_index + 1} of {len(self.playlist)}"
        counter = self.small_font.render(playlist_text, True, (160, 170, 190))
        self.screen.blit(counter, counter.get_rect(center=(self.WIDTH // 2, 390)))

    def handle_key(self, key):
        """Here is the keyboard control handler."""
        if key == pygame.K_p:
            self.play()
        elif key == pygame.K_s:
            self.stop()
        elif key == pygame.K_n:
            self.next_track()
        elif key == pygame.K_b:
            self.previous_track()

    def run(self):
        """Here is the main loop for the music player."""
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_q, pygame.K_ESCAPE):
                        running = False
                    else:
                        self.handle_key(event.key)

            if self.is_playing and not pygame.mixer.music.get_busy():
                self.is_playing = False

            self.draw()
            pygame.display.flip()
            self.timer.tick(30)

        pygame.mixer.music.stop()
        pygame.quit()

