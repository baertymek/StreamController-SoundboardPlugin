from enum import Enum

ID = "com_buggex_soundboard"

MAX_PLAYERS = 16

SETTING_DEVICE = "selected_device"
SETTING_PLAYER = "selected_player"

SETTING_SOUND_PATH        = "sound_path"
SETTING_SOUND_VOLUME      = "sound_volume"
SETTING_SOUND_IF_PLAYING  = "sound_if_playing"

class Players(Enum):
    Pygame = 0
    libVLC = 1

PLAYER_NAMES = {
  "Pygame": Players.Pygame,
  "libVLC": Players.libVLC
}

class BehaviorIfPlaying(Enum):
    Stop    = 0
    Restart = 1
    OnTop   = 2

BehaviorIfPlayingNames = {
    BehaviorIfPlaying.Stop:     "actions.play.if_playing.stop",
    BehaviorIfPlaying.Restart:  "actions.play.if_playing.restart",
    BehaviorIfPlaying.OnTop:    "actions.play.if_playing.on_top",
}