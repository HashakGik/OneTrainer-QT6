from PySide6.QtCore import QCoreApplication as QCA
from modules.ui.controllers.BaseController import BaseController

import PySide6.QtWidgets as QtW

from modules.ui.controllers.widgets.EmbeddingController import EmbeddingController

from modules.ui.models.StateModel import StateModel

class AdditionalEmbeddingsController(BaseController):
    children = []
    def __init__(self, loader, parent=None):
        super().__init__(loader, "modules/ui/views/tabs/additional_embeddings.ui", name=QCA.translate("main_window_tabs", "Additional Embeddings"), parent=parent)

    def _connectUIBehavior(self):
        self.connect(self.ui.addEmbeddingBtn.clicked, self.__appendEmbedding())

        cb = self.__updateEmbeddings()
        self.connect(QtW.QApplication.instance().embeddingsChanged, cb)
        self.connect(QtW.QApplication.instance().stateChanged, cb, update_after_connect=True)

        self.connect(self.ui.enableBtn.clicked, self.__enableEmbeddings())


    def __enableEmbeddings(self):
        def f():
            StateModel.instance().enable_embeddings()
            QtW.QApplication.instance().embeddingsChanged.emit()
        return f

    def __updateEmbeddings(self):
        def f():
            for c in self.children:
                c.disconnectAll()

            self.ui.listWidget.clear()
            self.children = []

            for idx, _ in enumerate(StateModel.instance().getState("additional_embeddings")):
                wdg = EmbeddingController(self.loader, idx, parent=self)
                self.children.append(wdg)
                self._appendWidget(self.ui.listWidget, wdg, self_delete_fn=self.__deleteEmbedding(idx), self_clone_fn=self.__cloneEmbedding(idx))

        return f

    def __cloneEmbedding(self, idx):
        def f():
            StateModel.instance().clone_embedding(idx)
            QtW.QApplication.instance().embeddingsChanged.emit()
        return f

    def __deleteEmbedding(self, idx):
        def f():
            StateModel.instance().delete_embedding(idx)
            QtW.QApplication.instance().embeddingsChanged.emit()
        return f

    def __appendEmbedding(self):
        def f():
            StateModel.instance().create_new_embedding()
            QtW.QApplication.instance().embeddingsChanged.emit()
        return f