from modules.ui.utils.base_controller import BaseController

from modules.ui.utils.figure_widget import FigureWidget

from PySide6.QtCore import QCoreApplication as QCA
import PySide6.QtWidgets as QtW

from modules.util.enum.BalancingStrategy import BalancingStrategy
from modules.util.enum.ConceptType import ConceptType
from modules.util.enum.TrainingMethod import TrainingMethod

from modules.ui.models.StateModel import StateModel


class ConceptController(BaseController):
    def __init__(self, loader, parent=None):
        super().__init__(loader, "modules/ui/views/windows/concept.ui", name=None, parent=parent)

        #self.canvas = FigureCanvas(Figure(figsize=(8, 3))) # TODO: refactor magic numbers. Possibly suggest a size in pixel for default rendering.
        self.canvas = FigureWidget(parent=self.ui, zoom_tools=True, navigation_tools=True, edit_tools=True)
        self.ui.histogramLay.addWidget(self.canvas.toolbar) # Matplotlib toolbar, in case we want the user to zoom in. TODO: add only relevant buttons (zoom, move, lin-log scale, etc.)
        self.ui.histogramLay.addWidget(self.canvas)

        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]
        ax = self.canvas.figure.subplots()
        ax.plot((x,y))


    # TODO: create CanvasWidget (subclass of FigureCanvas) to handle default color picking, etc., here just pass the data. Maybe even the entire canvas could be a class drawable=True/False
    #       modify ui replacing layout with QWidget promoted to CanvasWidget

    # TODO: FOR CONCEPT BUTTON DRAWING USE THIS INSTEAD: https://stackoverflow.com/questions/34697559/pil-image-to-qpixmap-conversion-issue

    """
    DRAWING:
    https://stackoverflow.com/questions/76571540/how-do-i-add-figurecanvasqtagg-in-a-pyqt-layout
    
    https://stackoverflow.com/questions/72242466/how-to-draw-on-an-image-tkinter-canvas-pil
    
    https://stackoverflow.com/questions/15721094/detecting-mouse-event-in-an-image-with-matplotlib
    https://matplotlib.org/3.2.2/users/event_handling.html#mouse-enter-and-leave
    https://scipy-cookbook.readthedocs.io/items/Matplotlib_Animations.html
    
    IDEA: 
    1)create canvas associated with PIL/numpy bitmask
    2)use mouse events to determine a start and end position
    3)draw a line on the bitmask
    4)bitblit the line on the canvas efficiently
    5)Use the bitmask for business logic
    
    BONUS: use matplotlib toolbox for draw/delete, instead of buttons + shortcuts
    https://matplotlib.org/stable/gallery/user_interfaces/toolmanager_sgskip.html 
    
    """

    def __enablePromptSource(self, _):
        if self.ui.promptSourceCmb.currentData() != "concept":
            self.ui.promptSourceLed.setEnabled(False)
            self.ui.promptSourceBtn.setEnabled(False)
        else:
            self.ui.promptSourceLed.setEnabled(True)
            self.ui.promptSourceBtn.setEnabled(True)

    def connectUIBehavior(self):
        self.connectFileDialog(self.ui.pathBtn, self.ui.pathLed, is_dir=True, title=QCA.translate("dialog_window", "Open Dataset directory"))
        self.connectFileDialog(self.ui.promptSourceBtn, self.ui.promptSourceLed, is_dir=False,
                               title=QCA.translate("dialog_window", "Open Prompt Source"),
                               filters=QCA.translate("filetype_filters",
                                                     "Text (*.txt)"))

        callback = self.__updateConceptType()
        QtW.QApplication.instance().modelChanged.connect(callback)
        callback(StateModel.instance().getState("model_type"), StateModel.instance().getState("training_method"))



    def __updateConceptType(self):
        # TODO: this enables prior prediction only when LORA is selected. However, this means that concepts may change type when training type is changed.
        def f(model_type, training_type):
            if training_type == TrainingMethod.LORA:
                context = "prior_pred_enabled"
            else:
                context = "prior_pred_disabled"
            self.ui.conceptTypeCmb.clear()
            for e in ConceptType.enabled_values(context=context):
                self.ui.conceptTypeCmb.addItem(e.pretty_print(), userData=e)

        return f

    def connectInputValidation(self):
        self.ui.promptSourceCmb.activated.connect(self.__enablePromptSource)

    def loadPresets(self):
        # TODO: if these flags are used only locally, just define values in ui files and handle logic with currentIndex. If they need to be saved in a config, factor them out in new enums.
        self.ui.promptSourceCmb.addItem(QCA.translate("prompt_source", "From text file per sample"), userData="sample")
        self.ui.promptSourceCmb.addItem(QCA.translate("prompt_source", "From single text file"), userData="concept")
        self.ui.promptSourceCmb.addItem(QCA.translate("prompt_source", "From image file name"), userData="filename")

        self.ui.dropoutModeCmb.addItem(QCA.translate("dropout_mode", "Full"), userData="FULL")
        self.ui.dropoutModeCmb.addItem(QCA.translate("dropout_mode", "Random"), userData="RANDOM")
        self.ui.dropoutModeCmb.addItem(QCA.translate("dropout_mode", "Random Weighted"), userData="RANDOM WEIGHTED")

        self.ui.specialDropoutTagsCmb.addItem(QCA.translate("special_dropout_tags", "None"), userData="NONE")
        self.ui.specialDropoutTagsCmb.addItem(QCA.translate("special_dropout_tags", "Blacklist"), userData="BLACKLIST")
        self.ui.specialDropoutTagsCmb.addItem(QCA.translate("special_dropout_tags", "Whitelist"), userData="WHITELIST")

        for e in BalancingStrategy.enabled_values():
            self.ui.balancingCmb.addItem(e.pretty_print(), userData=e)

        # TODO: this always allows Prior Validation concepts, even when LORA is not selected.
        #for e in ConceptType.enabled_values():
        #    self.ui.conceptTypeCmb.addItem(e.pretty_print(), userData=e)