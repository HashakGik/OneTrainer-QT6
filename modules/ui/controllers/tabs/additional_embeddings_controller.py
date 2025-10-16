from PySide6.QtCore import QCoreApplication as QCA
from modules.ui.controllers.controller_utils import AbstractController

from modules.ui.controllers.widgets.embedding_controller import EmbeddingController

class AdditionalEmbeddingsController(AbstractController):
    def __init__(self, loader, state=None, parent=None):
        super().__init__(loader, "modules/ui/views/tabs/additional_embeddings.ui", state=state, name=QCA.translate("main_window_tabs", "Additional Embeddings"), parent=parent)
        self.children = {}

    def connectUIBehavior(self):
        self.ui.addEmbeddingBtn.clicked.connect(lambda: self.__appendEmbedding())

    def __appendEmbedding(self):
        wdg = EmbeddingController(self.loader, len(self.children), state=self.state, parent=self)
        self.children[len(self.children)] = wdg
        self._appendWidget(self.ui.listWidget, wdg, self_delete_btn=True, self_clone_btn=True)