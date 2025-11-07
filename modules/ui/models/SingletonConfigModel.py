from PySide6.QtCore import QBasicMutex
from modules.util import path_util

import os

# Base class for config models. It provides a Singleton interface and a single mutex shared across all the subclasses.
class SingletonConfigModel:
    _instance = None
    config = None
    mutex = QBasicMutex()

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def getState(self, path):
        if self.config is not None:
            try:
                if self.mutex is not None:
                    self.mutex.lock()
                ref = self.config
                if path == "":
                    return ref
                for key in path.split("."):
                    if isinstance(ref, list):
                        ref = ref[int(key)]
                    elif hasattr(ref, key):
                        ref = getattr(ref, key)
                    else:
                        print("DEBUG: key {} not found in config".format(key))
                        break
                return ref
            except Exception as e:
                print("QUERY: {}. ERROR: {}".format(path, e))
            finally:
                if self.mutex is not None:
                    self.mutex.unlock()

        return None

    def setState(self, path, value):
        if self.config is not None:
            try:
                if self.mutex is not None:
                    self.mutex.lock()
                ref = self.config
                for ptr in path.split(".")[:-1]:
                    if isinstance(ref, list):
                        ref = ref[int(ptr)]
                    elif hasattr(ref, ptr):
                        ref = getattr(ref, ptr)
                if isinstance(ref, list):
                    ref[int(path.split(".")[-1])] = value
                elif hasattr(ref, path.split(".")[-1]):
                    setattr(ref, path.split(".")[-1], value)
                else:
                    print("DEBUG: key {} not found in config".format(path))
            except Exception as e:
                print("ERROR: {}".format(e))
                pass
            finally:
                if self.mutex is not None:
                    self.mutex.unlock()

    def load_available_config_names(self, dir="training_presets", include_default=True):
        if include_default:
            configs = [("", path_util.canonical_join(dir, "#.json"))]
        else:
            configs = []


        if os.path.isdir(dir):
            for path in os.listdir(dir):
                if path != "#.json":
                    path = path_util.canonical_join(dir, path)
                    if path.endswith(".json") and os.path.isfile(path):
                        name = os.path.basename(path)
                        name = os.path.splitext(name)[0]
                        configs.append((name, path))
            configs.sort()

        return configs