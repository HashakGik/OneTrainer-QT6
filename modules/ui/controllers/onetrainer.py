from modules.ui.utils.base_controller import BaseController

from modules.ui.controllers.tabs.general_controller import GeneralController
from modules.ui.controllers.tabs.model_controller import ModelController
from modules.ui.controllers.tabs.data_controller import DataController
from modules.ui.controllers.tabs.concepts_controller import ConceptsController
from modules.ui.controllers.tabs.training_controller import TrainingController
from modules.ui.controllers.tabs.sampling_controller import SamplingController
from modules.ui.controllers.tabs.backup_controller import BackupController
from modules.ui.controllers.tabs.tools_controller import ToolsController
from modules.ui.controllers.tabs.additional_embeddings_controller import AdditionalEmbeddingsController
from modules.ui.controllers.tabs.cloud_controller import CloudController
from modules.ui.controllers.tabs.lora_controller import LoraController
from modules.ui.controllers.tabs.embeddings_controller import EmbeddingsController

from modules.ui.controllers.windows.save_controller import SaveController

from modules.util.enum.TrainingMethod import TrainingMethod
from modules.util.enum.ModelType import ModelType

from modules.ui.utils.ModelFlags import ModelFlags

import webbrowser
from PySide6.QtCore import QCoreApplication as QCA
import PySide6.QtWidgets as QtW

from modules.util import path_util
from modules.util.path_util import write_json_atomic

import json
import os

# Main window.
class OnetrainerController(BaseController):
    state_ui_connections = {
        "model_type": "modelTypeCmb",
        "training_method": "trainingTypeCmb"
    }

    def __init__(self, loader, state=None, mutex=None):
        super().__init__(loader, "modules/ui/views/windows/onetrainer.ui", state=state, mutex=mutex, name="OneTrainer", parent=None)
        self.save_window = SaveController(self.loader, parent=self, state=state, mutex=mutex)
        self.children = {}
        self.__createTabs()

        cb1 = self.__updateModel()
        self.ui.modelTypeCmb.activated.connect(cb1)

        cb2 = self.__updateConfigs()
        QtW.QApplication.instance().stateChanged.connect(cb2)


        # At the beginning invalidate the gui.
        cb1()
        cb2()



    def __load_available_config_names(self, dir="training_presets"):
        configs = [("", path_util.canonical_join(dir, "#.json"))]
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

    def __updateConfigs(self):
        def f():
            configs = self.__load_available_config_names("training_presets") # TODO: refactor path
            self.ui.configCmb.clear()
            self.save_window.ui.configCmb.clear()
            for k, v in configs:
                self.ui.configCmb.addItem(k, userData=v)
                if not k.startswith("#"):
                    self.save_window.ui.configCmb.addItem(k, userData=v)
        return f

    def __updateModel(self):
        def f():
            flags = ModelFlags.getFlags(self.ui.modelTypeCmb.currentData(), self.ui.trainingTypeCmb.currentData())

            self.ui.trainingTypeCmb.clear()

            self.ui.trainingTypeCmb.addItem(QCA.translate("training_method", "Fine Tune"), userData=TrainingMethod.FINE_TUNE)
            self.ui.trainingTypeCmb.addItem(QCA.translate("training_method", "LoRA"), userData=TrainingMethod.LORA)

            if ModelFlags.CAN_TRAIN_EMBEDDING in flags:
                self.ui.trainingTypeCmb.addItem(QCA.translate("training_method", "Embedding"), userData=TrainingMethod.EMBEDDING)
            if ModelFlags.CAN_FINE_TUNE_VAE in flags:
                self.ui.trainingTypeCmb.addItem(QCA.translate("training_method", "Fine Tune VAE"), userData=TrainingMethod.FINE_TUNE_VAE)

            self.ui.trainingTypeCmb.activated.emit(0)


        return f

    def __createTabs(self):
        for name, controller in [
            ("general", GeneralController),
            ("model", ModelController),
            ("data", DataController),
            ("concepts", ConceptsController),
            ("training", TrainingController),
            ("sampling", SamplingController),
            ("backup", BackupController),
            ("tools", ToolsController),
            ("additional_embeddings", AdditionalEmbeddingsController),
            ("cloud", CloudController),
            ("lora", LoraController),
            ("embedding", EmbeddingsController)
        ]:
            c = controller(self.loader, parent=self, state=self.state, mutex=self.mutex)
            self.children[name] = {"controller": c, "index": len(self.children)}
            self.ui.tabWidget.addTab(c.ui, c.name)

        self.ui.tabWidget.setTabVisible(self.children["lora"]["index"], False)
        self.ui.tabWidget.setTabVisible(self.children["embedding"]["index"], False)


    def connectUIBehavior(self):
        self.ui.wikiBtn.clicked.connect(lambda: webbrowser.open("https://github.com/Nerogar/OneTrainer/wiki", new=0, autoraise=False))
        self.ui.saveConfigBtn.clicked.connect(lambda: self.openWindow(self.save_window, fixed_size=True))
        self.ui.exportBtn.clicked.connect(lambda: self.__exportConfig())

        self.ui.trainingTypeCmb.activated.connect(lambda _: self.__changeModel())
        self.ui.modelTypeCmb.activated.connect(lambda _: self.__changeModel())

        self.ui.configCmb.activated.connect(lambda idx: self.__loadConfig(self.ui.configCmb.currentData(), idx))

    def __loadConfig(self, config, idx=None):
        try:
            self.mutex.lock()
            if os.path.exists(config):
                with open(config, "r") as file:
                    self.state.from_dict(json.load(file))
        except Exception as e:
            print(e)
        finally:
            self.mutex.unlock()
        QtW.QApplication.instance().stateChanged.emit() # BUG: somehow this enters infinite loop?
        if idx is not None:
            self.ui.configCmb.setCurrentIndex(idx)

        # TODO: remember to emit stateChanged
        pass

    def __changeModel(self):
        model_type = self.ui.modelTypeCmb.currentData()
        training_type = self.ui.trainingTypeCmb.currentData()
        self.ui.tabWidget.setTabVisible(self.children["lora"]["index"], training_type == TrainingMethod.LORA)
        self.ui.tabWidget.setTabVisible(self.children["embedding"]["index"], training_type == TrainingMethod.EMBEDDING)

        # TODO: also training_type allowed values must change here...

        QtW.QApplication.instance().modelChanged.emit(model_type, training_type)
        QtW.QApplication.instance().aboutToQuit.connect(lambda: self.save_default()) # TODO: actually need to call __close() for tensorboard and workspace cleanup


    def __exportConfig(self):
        diag = QtW.QFileDialog()
        txt, flt = diag.getSaveFileName(parent=None, caption=QCA.translate("dialog_window", "Save Config"), dir=None,
                                        filter=QCA.translate("filetype_filters", "JSON (*.json)"))
        if txt != "":
            filename = self._appendExtension(txt, flt)
            self.mutex.lock()
            with open(filename, "w") as f:
                json.dump(self.state.to_pack_dict(secrets=False), f, indent=4)
            self.mutex.unlock()

    def _save_to_file(self, name):
        name = path_util.safe_filename(name)
        path = path_util.canonical_join("training_presets", f"{name}.json")

        write_json_atomic(path, self.state.to_settings_dict(secrets=False))

        return path

    def __save_secrets(self, path):
        write_json_atomic(path, self.state.secrets.to_dict())
        return path

    def save_default(self):
        self.mutex.lock()
        self._save_to_file("#")
        self.__save_secrets("secrets.json")
        self.mutex.unlock()

    def loadPresets(self):
        for k, v in [ #TODO simplify
            ("Stable Diffusion 1.5", ModelType.STABLE_DIFFUSION_15),
            ("Stable Diffusion 1.5 Inpainting", ModelType.STABLE_DIFFUSION_15_INPAINTING),
            ("Stable Diffusion 2.0", ModelType.STABLE_DIFFUSION_20),
            ("Stable Diffusion 2.0 Inpainting", ModelType.STABLE_DIFFUSION_20_INPAINTING),
            ("Stable Diffusion 2.1", ModelType.STABLE_DIFFUSION_21),
            ("Stable Diffusion 3", ModelType.STABLE_DIFFUSION_3),
            ("Stable Diffusion 3.5", ModelType.STABLE_DIFFUSION_35),
            ("Stable Diffusion XL 1.0 Base", ModelType.STABLE_DIFFUSION_XL_10_BASE),
            ("Stable Diffusion XL 1.0 Base Inpainting", ModelType.STABLE_DIFFUSION_XL_10_BASE_INPAINTING),
            ("Wuerstchen v2", ModelType.WUERSTCHEN_2),
            ("Stable Cascade", ModelType.STABLE_CASCADE_1),
            ("PixArt Alpha", ModelType.PIXART_ALPHA),
            ("PixArt Sigma", ModelType.PIXART_SIGMA),
            ("Flux Dev", ModelType.FLUX_DEV_1),
            ("Flux Fill Dev", ModelType.FLUX_FILL_DEV_1),
            ("Sana", ModelType.SANA),
            ("Hunyuan Video", ModelType.HUNYUAN_VIDEO),
            ("HiDream Full", ModelType.HI_DREAM_FULL),
            ("Chroma1", ModelType.CHROMA_1),
            ("QwenImage", ModelType.QWEN)
        ]:
            self.ui.modelTypeCmb.addItem(k, v)
