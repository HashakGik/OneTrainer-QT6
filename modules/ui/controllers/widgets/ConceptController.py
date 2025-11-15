from modules.ui.controllers.BaseController import BaseController

import PySide6.QtWidgets as QtW
import PySide6.QtGui as QtGui

from modules.ui.models.ConceptModel import ConceptModel

from PIL.ImageQt import ImageQt

class ConceptController(BaseController):
    def __init__(self, loader, concept_window, idx, parent=None):
        self.concept_window = concept_window
        self.idx = idx
        super().__init__(loader, "modules/ui/views/widgets/concept.ui", name=None, parent=parent)

        # TODO: static connections: enableCbx (text, enabled), conceptBtn (image)

    def _connectUIBehavior(self):
        self.connect(self.ui.conceptBtn.clicked, self.__openConceptWindow())
        self.connect(self.ui.enableCbx.clicked, self.__enableConcept())

        cb = self.__updateConcept()
        self.connect(QtW.QApplication.instance().conceptsChanged, cb)

        cb()

    def __openConceptWindow(self):
        def f():
            self.openWindow(self.concept_window, fixed_size=False)
            QtW.QApplication.instance().openConcept.emit(self.idx)
        return f

    def __enableConcept(self):
        def f():
            ConceptModel.instance().setState("{}.enabled".format(self.idx), self.ui.enableCbx.isChecked())
            QtW.QApplication.instance().conceptsChanged.emit()
        return f

    def __updateConcept(self):
        def f():
            self.ui.enableCbx.setChecked(ConceptModel.instance().getState("{}.enabled".format(self.idx)))
            self.ui.enableCbx.setText(ConceptModel.instance().get_concept_name(self.idx))

            img = ConceptModel.instance().get_preview_icon(self.idx)
            self.ui.conceptBtn.setIcon(QtGui.QIcon(QtGui.QPixmap.fromImage(ImageQt(img))))
        return f