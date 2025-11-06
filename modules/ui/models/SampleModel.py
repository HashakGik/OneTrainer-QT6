from PySide6.QtCore import QBasicMutex

from modules.ui.models.SingletonConfigModel import SingletonConfigModel
from modules.util.config.SampleConfig import SampleConfig
import copy

import os
import json

from modules.util.path_util import write_json_atomic
from modules.util import path_util

from modules.ui.models.StateModel import StateModel

class SampleModel(SingletonConfigModel):
    # _instance = None
    #
    # @classmethod
    # def instance(cls):
    #     if cls._instance is None:
    #         cls._instance = SampleModel()
    #
    #     return cls._instance

    def __init__(self):
        super().__init__()
        self.config = [] # SampleConfig.default_values()

    # def getState(self, path):
    #     if self.config is not None:
    #         try:
    #             if self.mutex is not None:
    #                 self.mutex.lock()
    #             ref = self.config
    #             if path == "":
    #                 return ref
    #             for key in path.split("."):
    #                 if isinstance(ref, list):
    #                     ref = ref[int(key)]
    #                 elif hasattr(ref, key):
    #                     ref = getattr(ref, key)
    #                 else:
    #                     print("DEBUG: key {} not found in config".format(key))
    #                     break
    #             return ref
    #         except Exception as e:
    #             print("QUERY: {}. ERROR: {}".format(path, e))
    #         finally:
    #             if self.mutex is not None:
    #                 self.mutex.unlock()
    #
    #     return None
    #
    # def setState(self, path, value):
    #     if self.config is not None:
    #         try:
    #             if self.mutex is not None:
    #                 self.mutex.lock()
    #             ref = self.config
    #             for ptr in path.split(".")[:-1]:
    #                 if isinstance(ref, list):
    #                     ref = ref[int(ptr)]
    #                 elif hasattr(ref, ptr):
    #                     ref = getattr(ref, ptr)
    #             if isinstance(ref, list):
    #                 ref[int(path.split(".")[-1])] = value
    #             elif hasattr(ref, path.split(".")[-1]):
    #                 setattr(ref, path.split(".")[-1], value)
    #             else:
    #                 print("DEBUG: key {} not found in config".format(path))
    #         except Exception as e:
    #             print("ERROR: {}".format(e))
    #             pass
    #         finally:
    #             if self.mutex is not None:
    #                 self.mutex.unlock()

    def __len__(self):
        return len(self.config)

    def get_default_sample(self):
        return SampleConfig.default_values().to_dict()

    def create_new_sample(self):
        try:
            self.mutex.lock()
            smp_cfg = SampleConfig.default_values()
            self.config.append(smp_cfg)
        except Exception as e:
            print(e)
        finally:
            self.mutex.unlock()

    def clone_sample(self, idx):
        try:
            self.mutex.lock()
            new_element = copy.deepcopy(self.config[idx])

            self.config.append(new_element)
        except Exception as e:
            print(e)
        finally:
            self.mutex.unlock()

    def delete_sample(self, idx):
        try:
            self.mutex.lock()
            self.config.pop(idx)

        except Exception as e:
            print(e)
        finally:
            self.mutex.unlock()

    def disable_samples(self):
        try:
            self.mutex.lock()
            for smp in self.config:
                smp.enabled = False

        except Exception as e:
            print(e)
        finally:
            self.mutex.unlock()

    # TODO: save/load json. Who invokes these?
    def save_config(self, path="training_samples"):
        if not os.path.exists(path):
            os.mkdir(path)

        try:
            config_path = StateModel.instance().getState("sample_definition_file_name") # IMPORTANT! The mutex is shared because it is defined in the base class, this must be called before the lock!

            self.mutex.lock()
            write_json_atomic(config_path,
                              [element.to_dict() for element in self.config])

        except Exception as e:
            print(e)
        finally:
            self.mutex.unlock()

    def load_config(self, filename, path="training_samples"):
        if not os.path.exists(path):
            os.mkdir(path)

        if filename == "":
            filename = "samples"

        try:
            config_file = path_util.canonical_join(path, "{}.json".format(filename))
            StateModel.instance().setState("sample_definition_file_name", config_file)

            self.mutex.lock()
            self.config = []

            if os.path.exists(config_file):

                with open(config_file, "r") as f:
                    loaded_config_json = json.load(f)
                    for element_json in loaded_config_json:
                        element = SampleConfig.default_values().from_dict(element_json)
                        self.config.append(element)

        except Exception as e:
            print(e)
        finally:
            self.mutex.unlock()