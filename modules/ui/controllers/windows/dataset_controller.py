from modules.ui.utils.base_controller import BaseController
from PySide6.QtCore import QCoreApplication as QCA
import PySide6.QtWidgets as QtW

from modules.ui.controllers.windows.caption_controller import CaptionController
from modules.ui.controllers.windows.mask_controller import MaskController

from modules.ui.utils.figure_widget import FigureWidget

class DatasetController(BaseController):
    def __init__(self, loader, parent=None):
        super().__init__(loader, "modules/ui/views/windows/dataset.ui", name=None, parent=parent)

        self.canvas = FigureWidget(parent=self.ui, width=7, height=5, zoom_tools=True, navigation_tools=True,
                                   edit_tools=True)

        self.ui.canvasLay.addWidget(self.canvas.toolbar)
        self.ui.canvasLay.addWidget(self.canvas)

        # TODO: NEW UI:
        # File browser with filters: by filename, by caption
        # Mask: undo/redo mask/delete/fill, clear all (reset mask + caption), reset (reset mask)
        # Multiple captions -> Apparently the combo box is a workaround to display multiple lines of captions because master branch would load only first line? Replace with QPlainText?

        # TODO: new windows: Image tools, Bulk Caption edit

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


        self.help_window = QtW.QMessageBox(QtW.QMessageBox.Icon.NoIcon, QCA.translate("dialog_window", "Dataset Tools Help"),
                                 QCA.translate("help_dataset", """
Keyboard shortcuts when focusing on the prompt input field:
Up arrow: previous image
Down arrow: next image
Return: save
Ctrl+M: only show the mask
Ctrl+D: draw mask editing mode
Ctrl+F: fill mask editing mode

When editing masks:
Left click: add mask
Right click: remove mask
Mouse wheel: increase or decrease brush size
"""))
        self.help_window.setModal(False)

        self.dataset = None
        self.mask_window = MaskController(loader, parent=self)
        self.caption_window = CaptionController(loader, parent=self)

    def __openDataset(self):
        diag = QtW.QFileDialog()
        dir = diag.getExistingDirectory(parent=None, caption=QCA.translate("dialog_window", "Open Dataset directory"), dir=self.dataset)

        # TODO: check if dir is a valid dataset folder, then assign:
        self.dataset = dir

    def connectUIBehavior(self):
        self.connect(self.ui.openBtn.clicked, self.__openDataset)
        self.connect(self.ui.generateMaskBtn.clicked, lambda: self.openWindow(self.mask_window, fixed_size=True))
        self.connect(self.ui.generateCaptionsBtn.clicked, lambda: self.openWindow(self.caption_window, fixed_size=True))
        self.connect(self.ui.helpBtn.clicked, lambda: self.help_window.show())