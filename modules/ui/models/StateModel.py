# modules/ui/ConfigList.py -> __load_available_config_names, __create_config, __add_config, __load_current_config, save_current_config
# modules/ui/TopBar.py -> __save_new_config, __load_current_config, __save_config,
import traceback

from modules.util.config.TrainConfig import TrainConfig, TrainEmbeddingConfig
from modules.util.config.SecretsConfig import SecretsConfig
from modules.ui.models.SingletonConfigModel import SingletonConfigModel

from modules.util import path_util
from modules.util.path_util import write_json_atomic

import json
import os
import copy


class StateModel(SingletonConfigModel):
    def __init__(self):
        super().__init__()

        self.config = TrainConfig.default_values()


    def save_default(self):
        self.mutex.lock()
        self.save_to_file("#")
        self.__save_secrets("secrets.json")
        self.mutex.unlock()

    def save_config(self, filename):
        self.mutex.lock()
        with open(filename, "w") as f:
            json.dump(self.config.to_pack_dict(secrets=False), f, indent=4)
        self.mutex.unlock()

    def load_config(self, filename):
        try:
            self.mutex.lock()
            basename = os.path.basename(filename)
            is_built_in_preset = basename.startswith("#") and basename != "#.json"

            if os.path.exists(filename):
                with open(filename, "r") as f:
                    loaded_dict = json.load(f)
                    default_config = TrainConfig.default_values()
                    if is_built_in_preset:
                        # always assume built-in configs are saved in the most recent version
                        loaded_dict["__version"] = default_config.config_version
                    loaded_config = default_config.from_dict(loaded_dict).to_unpacked_config()

                    if os.path.exists("secrets.json"):
                        with open("secrets.json", "r") as f:
                            secrets_dict = json.load(f)
                            loaded_config.secrets = SecretsConfig.default_values().from_dict(secrets_dict)

                    self.config.from_dict(loaded_config.to_dict())
        except Exception:
            print(traceback.format_exc())
        finally:
            self.mutex.unlock()

    def save_to_file(self, name):
        name = path_util.safe_filename(name)
        path = path_util.canonical_join("training_presets", f"{name}.json")

        write_json_atomic(path, self.config.to_settings_dict(secrets=False))

        return path

    def __save_secrets(self, path):
        write_json_atomic(path, self.config.secrets.to_dict())
        return path

    def create_new_embedding(self):
        try:
            self.mutex.lock()
            emb_cfg = TrainEmbeddingConfig.default_values()
            self.config.additional_embeddings.append(emb_cfg)
        except Exception as e:
            print(e)
        finally:
            self.mutex.unlock()

    def clone_embedding(self, idx):
        try:
            self.mutex.lock()
            new_element = copy.deepcopy(self.config.additional_embeddings[idx])
            new_element.uuid = self.get_random_uuid()

            self.config.additional_embeddings.append(new_element)
        except Exception as e:
            print(e)
        finally:
            self.mutex.unlock()

    def delete_embedding(self, idx):
        try:
            self.mutex.lock()
            self.config.additional_embeddings.pop(idx)

        except Exception as e:
            print(e)
        finally:
            self.mutex.unlock()

    def get_random_uuid(self):
        return TrainEmbeddingConfig.default_values().uuid