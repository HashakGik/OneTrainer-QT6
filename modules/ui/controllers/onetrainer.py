from modules.ui.controllers.controller_utils import AbstractController

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

import webbrowser
from PySide6.QtCore import QCoreApplication as QCA
import PySide6.QtWidgets as QtW

# Main window.
class OnetrainerController(AbstractController):
    def __init__(self, loader, state=None):
        super().__init__(loader, "modules/ui/views/windows/onetrainer.ui", state=state, name="OneTrainer", parent=None)
        self.save_window = SaveController(self.loader, parent=self)
        self.children = {}
        self.__createTabs()

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


    def setState(self, config):
        pass

    def getState(self):
        pass

    def getDefaultState(self):
        pass

    def connectUIBehavior(self):
        self.ui.wikiBtn.clicked.connect(lambda: webbrowser.open("https://github.com/Nerogar/OneTrainer/wiki", new=0, autoraise=False))
        self.ui.saveConfigBtn.clicked.connect(lambda: self.openWindow(self.save_window, fixed_size=True))
        self.ui.exportBtn.clicked.connect(lambda: self.__exportConfig())


        # TODO: add/remove tab for Embedding/Lora: self.ui.tabWidget.setTabVisible(self.children["lora"]["index"], True/False)
        # TODO: connect child tab elements depending on training and model type

    def connectInputValidation(self):
        pass

    def __exportConfig(self):
        diag = QtW.QFileDialog()
        txt, flt = diag.getSaveFileName(parent=None, caption=QCA.translate("dialog_window", "Save Config"), dir=None,
                                        filter=QCA.translate("filetype_filters", "JSON (*.json)"))
        filename = self._appendExtension(txt, flt)

        # TODO: use filename
        pass