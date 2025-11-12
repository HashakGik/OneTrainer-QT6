from modules.ui.controllers.base_controller import BaseController

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

from modules.ui.models.StateModel import StateModel

from modules.util.enum.TrainingMethod import TrainingMethod
from modules.util.enum.ModelType import ModelType

from modules.util.enum.ModelFlags import ModelFlags

import webbrowser
from PySide6.QtCore import QCoreApplication as QCA
import PySide6.QtWidgets as QtW


# Main window.
class OnetrainerController(BaseController):
    state_ui_connections = {
        "model_type": "modelTypeCmb",
        "training_method": "trainingTypeCmb"
    }

    def __init__(self, loader):
        super().__init__(loader, "modules/ui/views/windows/onetrainer.ui", name="OneTrainer", parent=None)
        self.save_window = SaveController(self.loader, parent=self)
        self.children = {}
        self.__createTabs()

        cb1 = self.__updateModel()
        self.connect(self.ui.modelTypeCmb.activated, cb1)

        cb2 = self.__updateConfigs()
        self.connect(QtW.QApplication.instance().stateChanged, cb2)


        # At the beginning invalidate the gui.
        cb1()
        cb2()

        # TODO: AT STARTUP LOAD #.json!

    def __updateConfigs(self):
        def f():
            configs = StateModel.instance().load_available_config_names("training_presets")
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
            c = controller(self.loader, parent=self)
            self.children[name] = {"controller": c, "index": len(self.children)}
            self.ui.tabWidget.addTab(c.ui, c.name)

        self.ui.tabWidget.setTabVisible(self.children["lora"]["index"], False)
        self.ui.tabWidget.setTabVisible(self.children["embedding"]["index"], False)


    def connectUIBehavior(self):
        self.connect(self.ui.wikiBtn.clicked, lambda: webbrowser.open("https://github.com/Nerogar/OneTrainer/wiki", new=0, autoraise=False))
        self.connect(self.ui.saveConfigBtn.clicked, lambda: self.openWindow(self.save_window, fixed_size=True))
        self.connect(self.ui.exportBtn.clicked, lambda: self.__exportConfig())

        self.connect(self.ui.trainingTypeCmb.activated, lambda _: self.__changeModel())
        self.connect(self.ui.modelTypeCmb.activated, lambda _: self.__changeModel())

        self.connect(self.ui.configCmb.activated, lambda idx: self.__loadConfig(self.ui.configCmb.currentData(), idx))

    def __loadConfig(self, config, idx=None):
        StateModel.instance().load_config(config)
        QtW.QApplication.instance().stateChanged.emit()
        QtW.QApplication.instance().embeddingsChanged.emit()
        if idx is not None:
            self.ui.configCmb.setCurrentIndex(idx)


    def __changeModel(self):
        model_type = self.ui.modelTypeCmb.currentData()
        training_type = self.ui.trainingTypeCmb.currentData()
        self.ui.tabWidget.setTabVisible(self.children["lora"]["index"], training_type == TrainingMethod.LORA)
        self.ui.tabWidget.setTabVisible(self.children["embedding"]["index"], training_type == TrainingMethod.EMBEDDING)

        # TODO: also training_type allowed values must change here...

        QtW.QApplication.instance().modelChanged.emit(model_type, training_type)
        self.connect(QtW.QApplication.instance().aboutToQuit, lambda: StateModel.instance().save_default()) # TODO: actually need to call __close() for tensorboard and workspace cleanup


    def __exportConfig(self):
        diag = QtW.QFileDialog()
        txt, flt = diag.getSaveFileName(parent=None, caption=QCA.translate("dialog_window", "Save Config"), dir=None,
                                        filter=QCA.translate("filetype_filters", "JSON (*.json)"))
        if txt != "":
            filename = self._appendExtension(txt, flt)
            StateModel.instance().save_config(filename)



    def loadPresets(self):
        for e in ModelType.enabled_values(context="main_window"):
            self.ui.modelTypeCmb.addItem(e.pretty_print(), userData=e)
