from modules.ui.models.SingletonConfigModel import SingletonConfigModel

from modules.util.config.ConceptConfig import ConceptConfig

import os
import json
import copy

from modules.util.path_util import write_json_atomic
from modules.util import path_util

from modules.ui.models.StateModel import StateModel

class ConceptModel(SingletonConfigModel):
    def __init__(self):
        self.config = []

    def __len__(self):
        return len(self.config)

    def get_random_seed(self):
        return ConceptConfig.default_values().seed

    def get_preview_image(self, idx):
        pass # TODO: from ConceptTab.py

    def get_concept_name(self, idx):
        pass # TODO: from ConceptTab.py

    def get_default_concept(self):
        pass # TODO: Is this required by someone?
        # return SampleConfig.default_values().to_dict()

    def create_new_concept(self):
        try:
            self.mutex.lock()
            # TODO
            con_cfg = ConceptConfig.default_values()
            self.config.append(con_cfg)
        except Exception as e:
            print(e)
        finally:
            self.mutex.unlock()

    def clone_concept(self, idx):
        try:
            self.mutex.lock()
            new_element = copy.deepcopy(self.config[idx])
            self.config.append(new_element)
        except Exception as e:
            print(e)
        finally:
            self.mutex.unlock()

    def delete_concept(self, idx):
        try:
            self.mutex.lock()
            self.config.pop(idx)

        except Exception as e:
            print(e)
        finally:
            self.mutex.unlock()

    def save_config(self, path="training_concepts"):
        if not os.path.exists(path):
            os.mkdir(path)

        try:
            config_path = StateModel.instance().getState("concept_file_name") # IMPORTANT! The mutex is shared because it is defined in the base class, this must be called before the lock!

            self.mutex.lock()
            write_json_atomic(config_path,
                              [element.to_dict() for element in self.config])

        except Exception as e:
            print(e)
        finally:
            self.mutex.unlock()

    def load_config(self, filename, path="training_concepts"):
        if not os.path.exists(path):
            os.mkdir(path)

        if filename == "":
            filename = "concepts"

        try:
            config_file = path_util.canonical_join(path, "{}.json".format(filename))
            StateModel.instance().setState("concept_file_name", config_file)

            self.mutex.lock()
            self.config = []

            if os.path.exists(config_file):

                with open(config_file, "r") as f:
                    loaded_config_json = json.load(f)
                    for element_json in loaded_config_json:
                        element = ConceptConfig.default_values().from_dict(element_json)
                        self.config.append(element)

        except Exception as e:
            print(e)
        finally:
            self.mutex.unlock()

    # TODO: ConceptWindow.py methods