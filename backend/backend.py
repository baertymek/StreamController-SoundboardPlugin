from streamcontroller_plugin_tools import BackendBase

from player_interface import PlayerInterface
from player_pygame import PlayerPygame
from player_vlc import PlayerVLC

from loguru import logger as log

import pygame
import pygame._sdl2.audio as sdl2_audio

# To get access to plugin files
import sys
from pathlib import Path
ABSOLUTE_PLUGIN_PATH = str(Path(__file__).parent.parent.absolute())
sys.path.insert(0, ABSOLUTE_PLUGIN_PATH)

from helpers import Consts
from helpers.Consts import Players

class SoundboardBackend(BackendBase):
    player : PlayerInterface

    def __init__(self):
        super().__init__()
        self.device = ""
        self.player_type = None
        self.players = {}
        self.free_ids = list(range(Consts.MAX_PLAYERS))

    def _allocate_id(self):
        if not self.free_ids:
            log.error("No free player IDs left")
        return self.free_ids.pop(0)

    def _free_id(self, id):
        self.free_ids.append(id)
        self.free_ids.sort()

    def set_player(self, playerType):
        player = Consts.PLAYER_NAMES[playerType]
        log.debug(f"new player: {playerType} {player}")
        self.player_type = player


    def set_device(self, device):
        self.device = device
        # if self.player is not None:
        #     self.player.set_device(device)

    def is_playing(self, player_id):
        if player_id not in self.players:
            return False

        player = self.players[player_id]
        if player is not None:
            return player.is_playing()

    def remaining_time(self, player_id):
        if player_id not in self.players:
            return -1

        player = self.players[player_id]
        if player:
            return player.remaining_time()

    def remaining_time_string(self, player_id):
        remaining_time = self.remaining_time(player_id)
        if remaining_time == -1:
            return "-1"
        if remaining_time is None:
            return None
        return str(f"{(remaining_time/1000):.1f}s")


    def play_sound(self, path_to_sound, volume) -> int:
        id = self._allocate_id()

        match self.player_type:
            case Players.Pygame:
                self.players[id] = PlayerPygame()
            case Players.libVLC:
                self.players[id] = PlayerVLC()
            case _:
                log.error(f"Unknown playerType {self.player_type}")

        if id not in self.players:
            log.error(f"Invalid player ID: {id}")
            return -1

        player = self.players[id]

        if player is not None:
            player.set_device(self.device)
            player.play_sound(path_to_sound, volume)

        return id

    def stop_sound(self, player_id):
        if player_id not in self.players:
            log.error(f"Invalid player ID: {player_id}")
            return

        player = self.players[player_id]
        if player is not None:
            player.stop_sound()
            del self.players[player_id]
            self._free_id(player_id)

    def stop_all_sound(self):
        for player_id in list(self.players.keys()):
            self.stop_sound(player_id)

    def get_audio_devices(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        return sdl2_audio.get_audio_device_names(False)

backend = SoundboardBackend()
