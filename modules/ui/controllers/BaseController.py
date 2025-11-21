import os
import functools
import PySide6.QtWidgets as QtW
import PySide6.QtCore as QtC

from PySide6.QtCore import Qt

import re
import webbrowser

from showinfm import show_in_file_manager

from modules.ui.utils.SNLineEdit import SNLineEdit

from modules.ui.models.StateModel import StateModel

# TODO: CLEANUP:
# 1) Naming convention is all over the place (camelCase, snake_case, inconsistent visibility __method vs _method vs method)
# 2) Some callbacks are invoked as lambdas, others as self.__method() which returns a function f(). Choose one!
# 4) Use self.openAlert to provide user feedback.
# 5) Uniform error logging (sometimes it is print, others it uses logger.logging) and exceptions (print(e) vs full traceback)
# 6) Mark every slot as @Slot for perfomance improvement

# Abstract controller with some utility methods.
class BaseController:
    state_ui_connections = {} # Class attribute, but it will be overwritten by every subclass.

    def __init__(self, loader, ui_file, name=None, parent=None, **kwargs):
        self.loader = loader
        self.parent = parent
        self.ui = loader.load(ui_file, parentWidget=parent.ui if parent is not None else None)
        self.name = name

        self.connections = {}
        self.invalidation_callbacks = []

        self._setup()

        self._loadPresets()

        self._connectStateUi(self.state_ui_connections, StateModel.instance(), signal=QtW.QApplication.instance().stateChanged, update_after_connect=True, **kwargs)
        self._connectUIBehavior()
        self._connectInputValidation()

        self._invalidateUI()

    # Use this method to initialize auxiliary attributes of each controller.
    def _setup(self):
        pass

    # Use this method to connect signals and slots for visual behavior.
    def _connectUIBehavior(self):
        pass

    # Use this method to handle complex field validation OTHER than the automatic validations defined in *.ui files.
    def _connectInputValidation(self):
        pass

    # Use this method to load preset values for each control.
    def _loadPresets(self):
        pass

    def _invalidateUI(self):
        for fn, *args in self.invalidation_callbacks:
            if len(args) > 0 and args[0] is not None:
                fn(*args)
            else:
                fn()

    def connect(self, signal, slot, key="global", update_after_connect=False, initial_args=None):
        c = signal.connect(slot)
        if key not in self.connections:
            self.connections[key] = []
        self.connections[key].append(c)

        # Schedule every update to be executed at the end of __init__
        if update_after_connect:
            if initial_args is None:
                self.invalidation_callbacks.append((slot, None))
            else:
                self.invalidation_callbacks.append((slot, *initial_args))

    def disconnectAll(self):
        for k, v in self.connections.items():
            for c in v:
                self.ui.disconnect(c)

        self.connections = {}

    def disconnectGroup(self, key):
        if key in self.connections:
            for c in self.connections[key]:
                self.ui.disconnect(c)
            self.connections[key] = []

    def _appendExtension(self, file, filter):
        patterns = filter.split("(")[1].split(")")[0].split(", ")
        for p in patterns:
            if re.match(p.replace(".", "\\.").replace("*", ".*"), file): # If the file already has a valid extension, return it as is.
                return file

        if "*" not in patterns[0]: # The pattern is a fixed filename, returning it regardless of the user selected name.
            return patterns[0] # TODO: maybe returning folder/patterns[0] is more reasonable? In original code there is: path_modifier=lambda x: Path(x).parent.absolute() if x.endswith(".json") else x (removes file and returns base folder instead)
        else:
            return "{}.{}".format(file, patterns[0].split("*.")[1]) # Append the first valid extension to file.


    def _connectStateUi(self, connection_dict, model, signal=None, update_after_connect=False, group="global", **kwargs):
        for var, ui_names in connection_dict.items():
            if len(kwargs) > 0:
                var = var.format(**kwargs)

            if isinstance(ui_names, str):
                ui_names = [ui_names]
            for ui_name in ui_names:
                ui_elem = self.ui.findChild(QtC.QObject, ui_name)
                if ui_elem is None:
                    print("ERROR: {} not found.".format(ui_name))
                else:
                    if isinstance(ui_elem, QtW.QCheckBox):
                        self.connect(ui_elem.stateChanged, self.__readCbx(ui_elem, var, model), group)
                    elif isinstance(ui_elem, QtW.QComboBox):
                        self.connect(ui_elem.activated, self.__readCbm(ui_elem, var, model), group)
                    elif isinstance(ui_elem, QtW.QSpinBox) or isinstance(ui_elem, QtW.QDoubleSpinBox):
                        self.connect(ui_elem.valueChanged, self.__readSbx(ui_elem, var, model), group)
                    elif isinstance(ui_elem, SNLineEdit): # IMPORTANT: keep this above base class!
                        self.connect(ui_elem.editingFinished, self.__readSNLed(ui_elem, var, model), group)
                    elif isinstance(ui_elem, QtW.QLineEdit):
                        self.connect(ui_elem.editingFinished, self.__readLed(ui_elem, var, model), group)

                    callback = functools.partial(BaseController._writeControl, ui_elem, var, model)
                    if signal is not None:
                        self.connect(signal, callback)
                    if update_after_connect:
                        callback()

    # These methods cannot use directly lambdas, because variable names would be reassigned within the loop.
    @staticmethod
    def __readCbx( ui_elem, var, model):
        return lambda: model.setState(var, ui_elem.isChecked())

    @staticmethod
    def __readCbm(ui_elem, var, model):
        return lambda: model.setState(var, ui_elem.currentData())

    @staticmethod
    def __readSbx(ui_elem, var, model):
        return lambda x: model.setState(var, x)

    @staticmethod
    def __readSNLed(ui_elem, var, model):
        return lambda: model.setState(var, float(ui_elem.text()))

    @staticmethod
    def __readLed(ui_elem, var, model):
        return lambda: model.setState(var, ui_elem.text())

    @staticmethod
    def _writeControl(ui_elem, var, model, *args): # Discard possible signal arguments.
        ui_elem.blockSignals(True)
        val = model.getState(var)
        if val is not None:
            if isinstance(ui_elem, QtW.QCheckBox):
                ui_elem.setChecked(val)
            elif isinstance(ui_elem, QtW.QComboBox):
                idx = ui_elem.findData(val)
                if idx != -1:
                    ui_elem.setCurrentIndex(idx)
            elif isinstance(ui_elem, QtW.QSpinBox) or isinstance(ui_elem, QtW.QDoubleSpinBox):
                ui_elem.setValue(float(val))
            elif isinstance(ui_elem, SNLineEdit): # IMPORTANT: keep this above base class!
                ui_elem.setText(str(val))
            elif isinstance(ui_elem, QtW.QLineEdit):
                ui_elem.setText(val)
        ui_elem.blockSignals(False)

    def _connectFileDialog(self, tool_button, edit_box, is_dir=False, save=False, title=None, filters=None):
        def f(elem):
            diag = QtW.QFileDialog()

            if is_dir:
                dir = None
                if os.path.isdir(elem.text()):
                    dir = elem.text()
                txt = diag.getExistingDirectory(parent=None, caption=title, dir=dir)
                elem.setText(self._removeWorkingDir(txt))
                elem.editingFinished.emit()
            else:
                file = None
                if os.path.exists(elem.text()):
                    file = self._removeWorkingDir(elem.text())

                if save:
                    txt, flt = diag.getSaveFileName(parent=None, caption=title, dir=file, filter=filters)
                    if txt != "":
                        elem.setText(self._removeWorkingDir(self._appendExtension(txt, flt)))
                        elem.editingFinished.emit()
                else:
                    txt, _ = diag.getOpenFileName(parent=None, caption=title, dir=file, filter=filters)
                    if txt != "":
                        elem.setText(self._removeWorkingDir(txt))
                        elem.editingFinished.emit()

        self.connect(tool_button.clicked, functools.partial(f, edit_box))

    def _removeWorkingDir(self, txt):
        cwd = os.getcwd()
        if txt.startswith(cwd):
            out = txt[len(cwd) + 1:]
            if out == "":
                out = "."
            return out # Remove working directory and trailing slash.
        else:
            return txt

    def _appendWidget(self, list_widget, controller, self_delete_fn=None, self_clone_fn=None):
        item = QtW.QListWidgetItem(list_widget)
        item.setSizeHint(controller.ui.size())
        list_widget.addItem(item)
        list_widget.setItemWidget(item, controller.ui)

        if self_delete_fn is not None:
            self.connect(controller.ui.deleteBtn.clicked, self_delete_fn)

        if self_clone_fn is not None:
            self.connect(controller.ui.cloneBtn.clicked, self_clone_fn)

    def _updateProgress(self, elem):
        def f(data):
            if "value" in data and "max_value" in data:
                val = int(elem.minimum() + data["value"] / data["max_value"] * (
                            elem.maximum() - elem.minimum())) if data["max_value"] > elem.minimum() else elem.minimum()
                if isinstance(elem, QtW.QProgressBar):
                    elem.setValue(val)
                elif isinstance(elem, QtW.QLabel):
                    elem.setText(str(val))
        return f

    def _log(self, severity, message):
        # TODO: if you prefer a GUI text area, print on it instead: https://stackoverflow.com/questions/24469662/how-to-redirect-logger-output-into-pyqt-text-widget
        # In that case it is important to register a global logger widget (e.g. on a window with different tabs for each severity level)
        # For high severity, maybe an alertbox can also be opened automatically
        StateModel.instance().log(severity, message) # TODO: refactor every message in the controller to use this. Do something similar with SingletonConfigModel

    def openWindow(self, controller, fixed_size=False):
        if fixed_size:
            controller.ui.setWindowFlag(Qt.WindowCloseButtonHint)
            controller.ui.setWindowFlag(Qt.WindowMaximizeButtonHint, on=False)
            controller.ui.setFixedSize(controller.ui.size())
        controller.ui.show()

    def openAlert(self, title, message, type="about", buttons=QtW.QMessageBox.StandardButton.Ok):
        wnd = None
        if type == "about":
            QtW.QMessageBox.about(self.ui, title, message) # About has no buttons nor return values.
        elif type == "critical":
            wnd = QtW.QMessageBox.critical(self.ui, title, message, buttons=buttons)
        elif type == "information":
            wnd = QtW.QMessageBox.information(self.ui, title, message, buttons=buttons)
        elif type == "question":
            wnd = QtW.QMessageBox.question(self.ui, title, message, buttons=buttons)
        elif type == "warning":
            wnd = QtW.QMessageBox.warning(self.ui, title, message, buttons=buttons)

        return wnd # TODO: check outcome with if openAlert(...) == QMessageBox.StandardButton.Ok


    def openUrl(self, url):
        webbrowser.open(url, new=0, autoraise=False)

    def browse(self, dir):
        if os.path.isdir(dir):
            show_in_file_manager(dir)
