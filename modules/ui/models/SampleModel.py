from modules.ui.models.SingletonConfigModel import SingletonConfigModel
from modules.util.config.SampleConfig import SampleConfig
import copy

import os
import json

from modules.util.path_util import write_json_atomic
from modules.util import path_util

from modules.ui.models.StateModel import StateModel

class SampleModel(SingletonConfigModel):
    def __init__(self):
        self.config = []

    def __len__(self):
        return len(self.config)

    @SingletonConfigModel.atomic
    def get_default_sample(self):
        return SampleConfig.default_values().to_dict()

    @SingletonConfigModel.atomic
    def create_new_sample(self):
        smp_cfg = SampleConfig.default_values()
        self.config.append(smp_cfg)

    @SingletonConfigModel.atomic
    def clone_sample(self, idx):
        new_element = copy.deepcopy(self.config[idx])
        self.config.append(new_element)

    @SingletonConfigModel.atomic
    def delete_sample(self, idx):
        self.config.pop(idx)

    @SingletonConfigModel.atomic
    def disable_samples(self):
        for smp in self.config:
            smp.enabled = False

    @SingletonConfigModel.atomic
    def save_config(self, path="training_samples"):
        if not os.path.exists(path):
            os.mkdir(path)

        config_path = StateModel.instance().getState("sample_definition_file_name")
        write_json_atomic(config_path, [element.to_dict() for element in self.config])

    @SingletonConfigModel.atomic
    def load_config(self, filename, path="training_samples"):
        if not os.path.exists(path):
            os.mkdir(path)

        if filename == "":
            filename = "samples"

        config_file = path_util.canonical_join(path, "{}.json".format(filename))
        StateModel.instance().setState("sample_definition_file_name", config_file)

        self.config = []

        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                loaded_config_json = json.load(f)
                for element_json in loaded_config_json:
                    element = SampleConfig.default_values().from_dict(element_json)
                    self.config.append(element)