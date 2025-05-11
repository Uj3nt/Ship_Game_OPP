import pygame
import random

class MusicPlayer:
    def __init__(self, playlist, volume=0.5, shuffle=False):
        pygame.mixer.init()
        self.playlist = playlist
        self.volume = volume
        self.shuffle = shuffle
        self.current_track = random.randint(0, len(playlist) - 1)
        self._setup_music()

        # Событие окончания трека
        self.MUSIC_END = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(self.MUSIC_END)

    def _setup_music(self):
        if self.shuffle:
            random.shuffle(self.playlist)
        pygame.mixer.music.set_volume(self.volume)

    def _load_track(self, index):
        try:
            pygame.mixer.music.load(self.playlist[index])
        except pygame.error as e:
            print(f"Ошибка загрузки трека {self.playlist[index]}: {e}")
            self.next_track()

    def next_track(self):
        self.current_track = (self.current_track + 1) % len(self.playlist)
        self._load_track(self.current_track)
        pygame.mixer.music.play()

    def play(self):
        if len(self.playlist) == 0:
            print("Плейлист пуст!")
            return

        self._load_track(self.current_track)
        pygame.mixer.music.play()

    def handle_events(self, event):
        if event.type == self.MUSIC_END:
            self.next_track()