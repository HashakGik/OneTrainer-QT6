from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.qt_compat import QtWidgets

import PySide6.QtWidgets as QtW
import PySide6.QtGui as QtG

from PySide6.QtCore import QCoreApplication as QCA
from PySide6.QtCore import Qt, Signal


from modules.util.enum.MouseButton import MouseButton
from modules.util.enum.ToolType import ToolType
from matplotlib.backend_bases import MouseButton as MplMouseButton
from matplotlib.figure import Figure


class MaskDrawingToolbar(NavigationToolbar):


    toolitems = [] # Override default matplotlib tools.

    def __init__(self, canvas, parent, zoom_tools=False, other_tools=None):
        super().__init__(canvas, parent, coordinates=False)
        self.widgets = []

        self.theme = "dark" if QtG.QGuiApplication.styleHints().colorScheme() == QtG.Qt.ColorScheme.Dark else "light"
        
        if zoom_tools: # Default matplotlib tools. We can reuse their callbacks (but we won't attach their shortcuts during tool use like fixing one axis, etc.).
            self.__addTool(self.home, type=ToolType.BUTTON,
                              name="home_btn",
                              #text=QCA.translate("toolbar_item", "Home View"),
                              icon="resources/icons/buttons/{}/house.svg".format(self.theme),
                              tooltip=QCA.translate("toolbar_item", "Reset original view (CTRL+H)"), shortcut="Ctrl+H")
            self.__addTool(self.pan, type=ToolType.CHECKABLE_BUTTON,
                              name="pan_btn",
                              #text=QCA.translate("toolbar_item", "Pan"),
                              icon="resources/icons/buttons/{}/move.svg".format(self.theme),
                              tooltip=QCA.translate("toolbar_item", "Left button pans, Right button zooms (CTRL+P)"), shortcut="Ctrl+P")
            self.__addTool(self.zoom, type=ToolType.CHECKABLE_BUTTON,
                              name="zoom_btn",
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

    def __addTool(self, fn, type, name=None, text=None, icon=None, tooltip=None, shortcut=None, spinbox_range=None): # TODO: ADD WIDGET NAME TO FIND IT LATER!
        wdg = None
        if type == ToolType.SEPARATOR:
            self.addSeparator()
        elif type == ToolType.SPINBOX:
            if spinbox_range is None:
                spinbox_range = (0.05, 1.0, 0.05)
            wdg = QtW.QLabel(self.canvas, text=text)
            wdg2 = QtW.QDoubleSpinBox(self.canvas, objectName=name)
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
            wdg = QtW.QToolButton(self.canvas, objectName=name)
            if shortcut is not None:
                scut = QtG.QShortcut(QtG.QKeySequence(shortcut), self.canvas)
                scut.setAutoRepeat(False)

            if type == ToolType.CHECKABLE_BUTTON:
                wdg.setCheckable(True)
                wdg.setAutoExclusive(True)

                # Connect shortcut to button click slot, handling checkable button's mutual exclusivity.
                def f():
                    # TODO: BUG: won't deactivate pan/zoom
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
    clicked = Signal(MouseButton, int, int) # x, y
    released = Signal(MouseButton, int, int) # x, y
    wheelUp = Signal()
    wheelDown = Signal()
    moved = Signal(MouseButton, int, int, int, int) # x0, y0, x1, y1.
    # Note: signals cannot be declared with unions like "int | None". So we either declare them as object to allow emitting None values, or use -1 for events outside the image (the latter approach is safer).

    def __init__(self, parent=None, width=5, height=4, dpi=100, zoom_tools=False, other_tools=None, emit_clicked=False, emit_released=False, emit_wheel=False, emit_moved=False, use_data_coordinates=True): # TODO: maybe add preferred size? Or use width/height in pixel and change figsize as the closest integer ratio (*10 // 10)?
        super().__init__(Figure(figsize=(width, height), dpi=dpi))
        self.toolbar = MaskDrawingToolbar(self, parent=parent, zoom_tools=zoom_tools, other_tools=other_tools)

        self.use_data_coordinates = use_data_coordinates
        self.last_x = self.last_y = None

        if emit_clicked:
            self.mpl_connect('button_press_event', self.__connectClicked())
        if emit_released:
            self.mpl_connect('button_release_event', self.__connectReleased())
        if emit_wheel:
            self.mpl_connect('scroll_event', self.__connectWheel())
        if emit_moved:
            self.mpl_connect('motion_notify_event', self.__connectMoved())

    def __connectClicked(self):
        def f(event):
            if self.use_data_coordinates:
                x, y = event.xdata, event.ydata
            else:
                x, y = event.x, event.y
            if event.button == MplMouseButton.LEFT:
                btn = MouseButton.LEFT
            elif event.button == MplMouseButton.RIGHT:
                btn = MouseButton.RIGHT
            elif event.button == MplMouseButton.MIDDLE:
                btn = MouseButton.MIDDLE
            else:
                btn = MouseButton.NONE

            self.last_x, self.last_y = x, y

            x = int(x) if x is not None else -1
            y = int(y) if y is not None else -1

            self.clicked.emit(btn, x, y)

        return f


    def __connectReleased(self):
        def f(event):
            if self.use_data_coordinates:
                x, y = event.xdata, event.ydata
            else:
                x, y = event.x, event.y
            if event.button == MplMouseButton.LEFT:
                btn = MouseButton.LEFT
            elif event.button == MplMouseButton.RIGHT:
                btn = MouseButton.RIGHT
            elif event.button == MplMouseButton.MIDDLE:
                btn = MouseButton.MIDDLE
            else:
                btn = MouseButton.NONE

            self.last_x = self.last_y = None

            x = int(x) if x is not None else -1
            y = int(y) if y is not None else -1

            self.released.emit(btn, x, y)
        return f

    def __connectMoved(self):
        def f(event):
            if self.use_data_coordinates:
                x1, y1 = event.xdata, event.ydata
            else:
                x1, y1 = event.x, event.y
            if event.button == MplMouseButton.LEFT:
                btn = MouseButton.LEFT
            elif event.button == MplMouseButton.RIGHT:
                btn = MouseButton.RIGHT
            elif event.button == MplMouseButton.MIDDLE:
                btn = MouseButton.MIDDLE
            else:
                btn = MouseButton.NONE

            x0, y0 = self.last_x, self.last_y

            self.last_x, self.last_y = x1, y1

            x0 = int(x0) if x0 is not None else -1
            y0 = int(y0) if y0 is not None else -1
            x1 = int(x1) if x1 is not None else -1
            y1 = int(y1) if y1 is not None else -1

            self.moved.emit(btn, x0, y0, x1, y1) # If -1, either start or finish is outside the canvas.
        return f


    def __connectWheel(self):
        def f(event):
            if event.button == "up":
                self.wheelUp.emit()
            elif event.button == "down":
                self.wheelDown.emit()
        return f