from modules.ui.models.SingletonConfigModel import SingletonConfigModel

from modules.util.config.BaseConfig import BaseConfig

class HistoryConfig(BaseConfig):
    buffer: list
    ptr: int

    @staticmethod
    def default_values():
        data = []

        # name, default value, data type, nullable
        data.append(("buffer", [], list, False))
        data.append(("ptr", 0, int, False))

        return HistoryConfig(data)

class HistoryModel(SingletonConfigModel):
    def __init__(self):
        self.config = HistoryConfig.default_values()

    @SingletonConfigModel.atomic
    def undo(self):
        if self.config.ptr > 0:
            self.config.ptr -= 1

    @SingletonConfigModel.atomic
    def redo(self):
        if self.config.ptr < len(self.config.buffer) - 1:
            self.config.ptr += 1

    @SingletonConfigModel.atomic
    def getCurrentState(self):
        if len(self.config.buffer) == 0:
            out = None
        else:
            out = self.config.buffer[self.config.ptr]
        return out

    @SingletonConfigModel.atomic
    def do(self, state):
        if self.config.ptr < len(self.config.buffer) - 1:
            self.config.buffer = self.config.buffer[:self.config.ptr + 1] # Invalidate the future before adding a new state.

        self.config.ptr = len(self.config.buffer)
        self.config.buffer.append(state)

    @SingletonConfigModel.atomic
    def clearHistory(self):
            self.config.buffer = []
            self.config.ptr = 0
