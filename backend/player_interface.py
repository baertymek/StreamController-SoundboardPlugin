from abc import ABC, abstractmethod

# creating interface
class PlayerInterface(ABC):

    @abstractmethod
    def set_device(self, device):
        pass

    @abstractmethod
    def is_playing(self):
        pass

    @abstractmethod
    def remaining_time(self):
        pass

    @abstractmethod
    def play_sound(self, path_to_sound, volume) -> int:
        pass

    @abstractmethod
    def stop_sound(self):
        pass