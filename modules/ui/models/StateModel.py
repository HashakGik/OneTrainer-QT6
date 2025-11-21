# modules/ui/ConfigList.py -> __load_available_config_names, __create_config, __add_config, __load_current_config, save_current_config
# modules/ui/TopBar.py -> __save_new_config, __load_current_config, __save_config,
import subprocess

from modules.util.config.TrainConfig import TrainConfig, TrainEmbeddingConfig
from modules.util.config.SecretsConfig import SecretsConfig
from modules.ui.models.SingletonConfigModel import SingletonConfigModel

from modules.util.enum.CloudType import CloudType

from modules.util import path_util
from modules.util.path_util import write_json_atomic

import json
import os
import copy
import sys
from pathlib import Path

import faulthandler
from scalene import scalene_profiler # TODO: importing Scalene sets the application locale to ANSI-C, while QT6 uses UTF-8 by default. We could change locale to C to suppress warnings, but this may cause problems with some features...


class StateModel(SingletonConfigModel):
    def __init__(self):
        self.config = TrainConfig.default_values()
        self.is_profiling = False
        self.tensorboard_subprocess = None


    def save_default(self):
        self.save_to_file("#")
        self.__save_secrets("secrets.json")

    def save_config(self, filename):
        with self.critical_region():
            with open(filename, "w") as f:
                json.dump(self.config.to_pack_dict(secrets=False), f, indent=4)

    def load_config(self, filename):
        with self.critical_region():
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

    def save_to_file(self, name):
        name = path_util.safe_filename(name)
        path = path_util.canonical_join("training_presets", f"{name}.json")

        with self.critical_region():
            write_json_atomic(path, self.config.to_settings_dict(secrets=False))

        return path

    def __save_secrets(self, path):
        with self.critical_region():
            write_json_atomic(path, self.config.secrets.to_dict())
        return path

    def setSchedulerParams(self, idx, key, value):
        # TODO: Check that no two keys are shared?
        with self.critical_region():
            if len(self.config.scheduler_params) == idx:
                self.config.scheduler_params.append({"key": key, "value": value})
            elif len(self.config.scheduler_params) > idx:
                self.config.scheduler_params[idx] = {"key": key, "value": value}

    def create_new_embedding(self):
        with self.critical_region():
            emb_cfg = TrainEmbeddingConfig.default_values()
            self.config.additional_embeddings.append(emb_cfg)

    def clone_embedding(self, idx):
        with self.critical_region():
            new_element = copy.deepcopy(self.config.additional_embeddings[idx])
            new_element.uuid = self.get_random_uuid()

            self.config.additional_embeddings.append(new_element)

    def delete_embedding(self, idx):
        with self.critical_region():
            self.config.additional_embeddings.pop(idx)

    def get_random_uuid(self):
        return TrainEmbeddingConfig.default_values().uuid

    def dump_stack(self):
        with open('stacks.txt', 'w') as f:
            faulthandler.dump_traceback(f)

    def toggle_profiler(self):
        if self.is_profiling:
            scalene_profiler.stop()
        else:
            scalene_profiler.start()

    def start_tensorboard(self):
        if self.tensorboard_subprocess:
            self.stop_tensorboard()

        tensorboard_executable = os.path.join(os.path.dirname(sys.executable), "tensorboard")
        tensorboard_log_dir = os.path.join(self.getState("workspace_dir"), "tensorboard")

        os.makedirs(Path(tensorboard_log_dir).absolute(), exist_ok=True)

        tensorboard_args = [
            tensorboard_executable,
            "--logdir",
            tensorboard_log_dir,
            "--port",
            str(self.getState("tensorboard_port")),
            "--samples_per_plugin=images=100,scalars=10000",
        ]

        if self.getState("tensorboard_expose"):
            tensorboard_args.append("--bind_all")

        try:
            self.tensorboard_subprocess = subprocess.Popen(tensorboard_args)
        except Exception:
            self.tensorboard_subprocess = None

    def stop_tensorboard(self):
        if self.tensorboard_subprocess:
            try:
                self.tensorboard_subprocess.terminate()
                self.tensorboard_subprocess.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.tensorboard_subprocess.kill()
            except Exception:
                pass
            finally:
                self.tensorboard_subprocess = None

    def enable_embeddings(self):
        add_embs = len(self.getState("additional_embeddings"))
        for idx in range(add_embs):
            self.setState("additional_embeddings.{}.train".format(idx), True)

    def get_gpus(self):
        gpus = []

        if self.getState("cloud.type") == CloudType.RUNPOD:
            import runpod
            runpod.api_key = self.getState("secrets.cloud.api_key")
            gpus = runpod.get_gpus()

        return gpus