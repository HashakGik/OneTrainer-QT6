import functools

from PIL.ImageQt import QPixmap
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.figure import Figure

import PySide6.QtWidgets as QtW
import PySide6.QtGui as QtG

from PySide6.QtCore import QCoreApplication as QCA
from PySide6.QtCore import Qt

from enum import Enum, auto


# TODO: NEW FEATURES:
# Undo/redo mask
# Multiple captions (combobox)
# Filters on files: by caption/by filename
# Image tools window
# Bulk caption editor?
# Browse button

class ToolType(Enum):
    SEPARATOR = auto()
    BUTTON = auto()
    CHECKABLE_BUTTON = auto()
    SPINBOX = auto()

class MaskDrawingToolbar(NavigationToolbar):


    toolitems = [] # Override default matplotlib tools.

    def __init__(self, canvas, parent, zoom_tools=False, other_tools=None):
        super().__init__(canvas, parent, coordinates=False)
        self.widgets = []

        self.theme = "dark" if QtG.QGuiApplication.styleHints().colorScheme() == QtG.Qt.ColorScheme.Dark else "light"
        
        if zoom_tools: # Default matplotlib tools. We can reuse their callbacks (but we won't attach their shortcuts during tool use like fixing one axis, etc.).
            self.__addTool(self.home, type=ToolType.BUTTON,
                              #text=QCA.translate("toolbar_item", "Home View"),
                              icon="resources/icons/buttons/{}/house.svg".format(self.theme),
                              tooltip=QCA.translate("toolbar_item", "Reset original view (CTRL+H)"), shortcut="Ctrl+H")
            self.__addTool(self.pan, type=ToolType.CHECKABLE_BUTTON,
                              #text=QCA.translate("toolbar_item", "Pan"),
                              icon="resources/icons/buttons/{}/move.svg".format(self.theme),
                              tooltip=QCA.translate("toolbar_item", "Left button pans, Right button zooms (CTRL+P)"), shortcut="Ctrl+P")
            self.__addTool(self.zoom, type=ToolType.CHECKABLE_BUTTON,
                              #text=QCA.translate("toolbar_item", "Zoom"),
                              icon="resources/icons/buttons/{}/search.svg".format(self.theme),
                              tooltip=QCA.translate("toolbar_item", "Zoom to rectangle (CTRL+Q)"), shortcut="Ctrl+Q")
            
            if other_tools is not None:
                self.addSeparator()
        
        if other_tools is not None:
            self.__addTools(other_tools)
        

    def __addTools(self, tools):
        for t in tools:
            self.__addTool(*t)

    def __addTool(self, fn, type, text=None, icon=None, tooltip=None, shortcut=None, spinbox_range=None):
        # TODO: ADD LIST OF WIDGETS TO CHECK/UNCHECK THEM
        wdg = None
        if type == ToolType.SEPARATOR:
            self.addSeparator()
        elif type == ToolType.SPINBOX:
            if spinbox_range is None:
                spinbox_range = (0.05, 1.0, 0.05)
            wdg = QtW.QLabel(self.canvas, text=text)
            wdg2 = QtW.QDoubleSpinBox(self.canvas)
            wdg2.setMinimum(spinbox_range[0])
            wdg2.setMaximum(spinbox_range[1])
            wdg2.setSingleStep(spinbox_range[2])
            wdg2.valueChanged.connect(fn)

            wdg.setBuddy(wdg2)
            if icon is not None:
                wdg.setPixmap(QtG.QPixmap(icon))
            if tooltip is not None:
                wdg2.setToolTip(tooltip)
            self.addWidget(wdg)
            self.addWidget(wdg2)
            self.widgets.append(wdg2)

        else:
            wdg = QtW.QToolButton(self.canvas)
            if shortcut is not None:
                scut = QtG.QShortcut(QtG.QKeySequence(shortcut), self.canvas)
                scut.setAutoRepeat(False)

            if type == ToolType.CHECKABLE_BUTTON:
                wdg.setCheckable(True)
                wdg.setAutoExclusive(True)

                # Connect shortcut to button click slot, handling checkable button's mutual exclusivity.
                def f():
                    for w in self.widgets: # Manually decheck everything, because autoExclusive forces at least one to be checked.
                        if isinstance(w, QtW.QToolButton) and w.isCheckable() and w != wdg:
                            w.setAutoExclusive(False)
                            w.setChecked(False)
                            w.setAutoExclusive(True)
                    wdg.setAutoExclusive(False)
                    wdg.click()
                    wdg.setAutoExclusive(True)

                scut.activated.connect(f)
            else:
                scut.activated.connect(wdg.click)


            wdg.clicked.connect(fn)

            if text is not None and icon is not None:
                wdg.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

            if text is not None:
                wdg.setText(text)

            if icon is not None:
                wdg.setIcon(QtG.QIcon(icon))

            if tooltip is not None:
                wdg.setToolTip(tooltip)

            self.addWidget(wdg)
            self.widgets.append(wdg)


class FigureWidget(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100, zoom_tools=False, other_tools=None): # TODO: maybe add preferred size? Or use width/height in pixel and change figsize as the closest integer ratio (*10 // 10)?
        super().__init__(Figure(figsize=(width, height), dpi=dpi))
        self.toolbar = MaskDrawingToolbar(self, parent=parent, zoom_tools=zoom_tools, other_tools=other_tools)


    def drawImage(self, image, ax, alpha=1.0, layer=0):
        #self.images[layer] = (image, alpha)

        print(self.figure.__dict__)
        ax.imshow(image) # ok, but shows only last image. Approach: im = imshow(first_image), then im.set_data(np.array))
        # This means that this method becomes the MaskModel's responsibility

        self.draw_idle()

        print(image) # TODO: save (image, alpha) in self.images[layer] and draw them in order.
        # TODO: remember to update with draw_idle() to do it asynchronously!!!
        pass