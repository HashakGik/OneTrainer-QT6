import functools

from PIL.ImageQt import QPixmap
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.figure import Figure

import PySide6.QtWidgets as QtW
import PySide6.QtGui as QtG

from PySide6.QtCore import QCoreApplication as QCA


# TODO: NEW FEATURES:
# Undo/redo mask
# Multiple captions (combobox)
# Filters on files: by caption/by filename
# Image tools window
# Bulk caption editor?
# Browse button

class MaskDrawingToolbar(NavigationToolbar):
    #toolitems = [
    #    ("Home", "This is the Home Button, don't forget to translate it", "home", "home"),
    #    # This is a list of buttons defined by tuples of four STRINGS: ("name", "tooltip", "icon (relative to <matplotlib path>/mpl-data/images and without extension)", "callback resolved as self.callback()")
    #    (None, None, None, None), # This is a spacer
    #]
    toolitems = []

    def f(self):
        pass # TODO: DUMMY CALLBACK

    def __init__(self, canvas, parent, zoom_tools=False, navigation_tools=False, edit_tools=False):
        super().__init__(canvas, parent, coordinates=False)

        # TODO: replace callbacks (eg. self.save()). NOTE: save, reset, edit mask, etc. need to operate on properties of canvas (FigureWidget), which also needs to expose getter/setter (better self.canvas.save() directly?)
        """
        DEFAULT PAN METHOD IMPLEMENTATION:
        
            def pan(self, *args):
                if not self.canvas.widgetlock.available(self):
                    self.set_message("pan unavailable")
                    return
                if self.mode == _Mode.PAN:
                    self.mode = _Mode.NONE
                    self.canvas.widgetlock.release(self)
                else:
                    self.mode = _Mode.PAN
                    self.canvas.widgetlock(self)
                for a in self.canvas.figure.get_axes():
                    a.set_navigate_mode(self.mode._navigate_mode)
        
        """

        self.theme = "dark" if QtG.QGuiApplication.styleHints().colorScheme() == QtG.Qt.ColorScheme.Dark else "light"

        if navigation_tools:
            self.__appendTool(functools.partial(MaskDrawingToolbar.f, self),
                              #text=QCA.translate("toolbar_item", "Previous"),
                              icon="resources/icons/buttons/{}/arrow-left.svg".format(self.theme),
                              tooltip=QCA.translate("toolbar_item", "Previous image (shortcut: <Left Arrow>"), shortcut="Left")
            self.__appendTool(functools.partial(MaskDrawingToolbar.f, self),
                              #text=QCA.translate("toolbar_item", "Next"),
                              icon="resources/icons/buttons/{}/arrow-right.svg".format(self.theme),
                              tooltip=QCA.translate("toolbar_item", "Next image (shortcut: <Right Arrow>"), shortcut="Right")


            if zoom_tools or edit_tools:
                self.addSeparator()
        if zoom_tools: # Default matplotlib tools. We can reuse their callbacks (but we won't attach their shortcuts during tool use like fixing one axis, etc.).
            self.__appendTool(self.home,
                              #text=QCA.translate("toolbar_item", "Home View"),
                              icon="resources/icons/buttons/{}/house.svg".format(self.theme),
                              tooltip=QCA.translate("toolbar_item", "Reset original view (CTRL+H)"), shortcut="Ctrl+H")
            self.__appendTool(self.pan,
                              #text=QCA.translate("toolbar_item", "Pan"),
                              icon="resources/icons/buttons/{}/move.svg".format(self.theme),
                              tooltip=QCA.translate("toolbar_item", "Left button pans, Right button zooms (CTRL+P)"), checkable=True, shortcut="Ctrl+P")
            self.__appendTool(self.zoom,
                              #text=QCA.translate("toolbar_item", "Zoom"),
                              icon="resources/icons/buttons/{}/search.svg".format(self.theme),
                              tooltip=QCA.translate("toolbar_item", "Zoom to rectangle (CTRL+Z)"), checkable=True, shortcut="Ctrl+Z")
            if edit_tools:
                self.addSeparator()
        if edit_tools:
            # TODO: if possible, callbacks should be handled by DatasetModel (wrapped here for encapsulation of confirm dialog and to keep the model GUI agnostic)

            self.__appendTool(functools.partial(MaskDrawingToolbar.f, self),
                              #text=QCA.translate("toolbar_item", "Edit Mask"),
                              icon="resources/icons/buttons/{}/brush.svg".format(self.theme),
                              tooltip=QCA.translate("toolbar_item", "Draw (<Left click>) or Erase (<Right click>) mask (CTRL+E)"), checkable=True, shortcut="Ctrl+E")
            self.__appendTool(functools.partial(MaskDrawingToolbar.f, self),
                              #text=QCA.translate("toolbar_item", "Fill Mask"),
                              icon="resources/icons/buttons/{}/paint-bucket.svg".format(self.theme),
                              tooltip=QCA.translate("toolbar_item",
                                                    "Fill (<Left click>) or Erase-fill (<Right click>) mask (CTRL+F)"), checkable=True, shortcut="Ctrl+F")
            self.__appendTool(functools.partial(MaskDrawingToolbar.f, self),
                              text=QCA.translate("toolbar_item", "Brush size"),
                              tooltip=QCA.translate("toolbar_item",
                                                    "Brush size (shortcut: <Mouse wheel up> or <Mouse wheel down>)"),
                                                    is_spinbox=True, spinbox_range=(0.05, 1.0, 0.05)) # TODO: CHECK
            self.__appendTool(functools.partial(MaskDrawingToolbar.f, self),
                              text=QCA.translate("toolbar_item", "Brush opacity"),
                              tooltip=QCA.translate("toolbar_item",
                                                    "Brush opacity"),
                              is_spinbox=True, spinbox_range=(0.05, 1.0, 0.05))  # TODO: CHECK
            self.addSeparator()


            self.addSeparator()
            self.__appendTool(functools.partial(MaskDrawingToolbar.f, self),
                              text=QCA.translate("toolbar_item", "Clear All"),
                              tooltip=QCA.translate("toolbar_item",
                                                    "Clear all (CTRL+Del)"), shortcut="Ctrl+Del") # TODO: the callback should ask for confirmation
            self.__appendTool(functools.partial(MaskDrawingToolbar.f, self),
                              text=QCA.translate("toolbar_item", "Reset Mask"),
                              tooltip=QCA.translate("toolbar_item",
                                                    "Reset mask (CTRL+R)"), shortcut="Ctrl+R") # TODO: the callback should ask for confirmation

            self.addSeparator()
            self.__appendTool(functools.partial(MaskDrawingToolbar.f, self),
                              #text=QCA.translate("toolbar_item", "Save Mask"),
                              icon="resources/icons/buttons/{}/save.svg".format(self.theme),
                              tooltip=QCA.translate("toolbar_item",
                                                    "Save mask (CTRL+S)"), shortcut="Ctrl+S")
            self.__appendTool(functools.partial(MaskDrawingToolbar.f, self),
                              # text=QCA.translate("toolbar_item", "Undo"),
                              icon="resources/icons/buttons/{}/undo.svg".format(self.theme),
                              tooltip=QCA.translate("toolbar_item",
                                                    "Undo (CTRL+Z)"), shortcut="Ctrl+Z")
            self.__appendTool(functools.partial(MaskDrawingToolbar.f, self),
                              # text=QCA.translate("toolbar_item", "Redo"),
                              icon="resources/icons/buttons/{}/redo.svg".format(self.theme),
                              tooltip=QCA.translate("toolbar_item",
                                                    "Undo (CTRL+Y)"), shortcut="Ctrl+Y")

            # TODO: add manual shortcuts for spinbox up/down.





    def __appendTool(self, callback, text=None, icon=None, tooltip=None, is_spinbox=False, spinbox_range=(0.05, 1.0, 0.05), checkable=False, shortcut=None):
        if is_spinbox:
            wdg = QtW.QLabel(self.canvas, text=text)
            wdg2 = QtW.QDoubleSpinBox(self.canvas)
            wdg2.setMinimum(spinbox_range[0])
            wdg2.setMaximum(spinbox_range[1])
            wdg2.setSingleStep(spinbox_range[2])
            wdg2.valueChanged.connect(callback)

            wdg.setBuddy(wdg2)
            if icon is not None:
                wdg.setIcon(QtG.QIcon(icon))
            if tooltip is not None:
                wdg2.setToolTip(tooltip)
            self.addWidget(wdg)
            self.addWidget(wdg2)
        else:
            wdg = QtW.QToolButton(self.canvas)
            wdg.setCheckable(checkable)
            wdg.setAutoExclusive(checkable)
            if shortcut is not None:
                scut = QtG.QShortcut(QtG.QKeySequence(shortcut), self.canvas)
                scut.setAutoRepeat(False)
                if checkable:
                    # Workaround for toggling the button with a shortcut.
                    # The intended behavior of autoExclusive (https://stackoverflow.com/questions/75376824/uncheck-a-qpushbutton-with-autoexclusive) is to always keep at least one element checked.
                    # Oddly enough, this does not interfere with a "natural" click event.
                    def f():
                        # TODO: BUG: this workaround does not decheck other buttons
                        print("BEFORE: {}".format(wdg.isChecked()))

                        wdg.setAutoExclusive(False)
                        #wdg.toggle() # click()
                        wdg.click()
                        print("AFTER: {}".format(wdg.isChecked()))
                        wdg.setAutoExclusive(True)

                        """
                        autoexclusive off -> click -> autoexclusive on: single tool works, but alternating tools do not deactivate each other and can desynchronize
                        toggle -> click: can switch tools correctly, but twice the same shortcut does not deactivate current tool graphically (while internal tool state is changed correctly)
                        """

                    scut.activated.connect(f)
                else:
                    scut.activated.connect(wdg.click)


            wdg.clicked.connect(callback)

            if text is not None:
                wdg.setText(text)

            if icon is not None:
                wdg.setIcon(QtG.QIcon(icon))

            if tooltip is not None:
                wdg.setToolTip(tooltip)

            self.addWidget(wdg)

    """
Onetrainer windows:
    histogram concept
    image augmentation (PIL updated with new image)
    timestep distribution
    sampling tool (PIL? Home/Pan/Zoom?)
    dataset tool (Draw/Fill/Erase/Home/Pan/Zoom/Save/Alpha spinbox/Prev img/Next img/Show-hide mask)

Standard QIcon icons: https://www.pythonguis.com/faq/built-in-qicons-pyqt/
    
    """

class FigureWidget(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100, navigation_tools=False, zoom_tools=False, edit_tools=False): # TODO: maybe add preferred size? Or use width/height in pixel and change figsize as the closest integer ratio (*10 // 10)?
        super().__init__(Figure(figsize=(width, height), dpi=dpi))
        self.toolbar = MaskDrawingToolbar(self, parent=parent, navigation_tools=navigation_tools, zoom_tools=zoom_tools, edit_tools=edit_tools)

        # TODO: CUSTOM BUTTONS MUST DISABLE DEFAULT MATPLOTLIB TOOLS

        # toolitems is a list of tuples:
        """
        [
        ("name", "tooltip", "image", "callback"), # Callback is a string referring to a method in self -> subclass NavigationToolbar https://stackoverflow.com/questions/12695678/how-to-modify-the-navigation-toolbar-easily-in-a-matplotlib-figure-window
        ...
        
        ]
        """

        # TODO: personalize toolbar (apparently self.toolbar.addWidget(Qwhatever) can add arbitrary widgets and their signals can be .connect() as usual). toolbar=bool, drawable=bool
        # TODO: policy minimum (allow only growing with respect to preferred size)?
        # TODO: remember to update with draw_idle() to do it asynchronously!!!

