import os
import functools
import PySide6.QtWidgets as QtW
import PySide6.QtCore as QtC

from PySide6.QtCore import Slot, Qt

import re

from modules.ui.utils.sn_line_edit import SNLineEdit


# Abstract controller with some utility methods.
class BaseController:
    state_ui_connections = {}

    def __init__(self, loader, ui_file, state=None, mutex=None, name=None, parent=None):
        self.loader = loader
        self.parent = parent
        self.ui = loader.load(ui_file, parentWidget=parent.ui if parent is not None else None)
        self.name = name # TODO: When necessary, derived classes will set this with QCA.translate(context, "STATIC STRING") since lupdate is a static analyzer!
        self.state = state
        self.mutex = mutex

        self.setup()

        self.connectUIBehavior()
        self.connectInputValidation()
        self.loadPresets()
        self.__connectStateUi()

        # TODO: IMPORTANT!!! For IO-bound calls use ASYNC SLOTS!: https://stackoverflow.com/questions/74196406/pyqt6-asyncio-connect-an-async-function-as-a-slot

    # TODO: refactor to use this method for OptimizerControlelr and TrainingController, to make connections cleaner
    # This is called before elements are connected together, therefore it can be used to create dynamic GUI elements programmatically.
    def setup(self):
        pass

    def _appendExtension(self, file, filter):
        patterns = filter.split("(")[1].split(")")[0].split(", ")
        for p in patterns:
            if re.match(p.replace(".", "\\.").replace("*", ".*"), file): # If the file already has a valid extension, return it as is.
                return file

        if "*" not in patterns[0]: # The pattern is a fixed filename, returning it regardless of the user selected name.
            return patterns[0] # TODO: maybe returning folder/patterns[0] is more reasonable? In original code there is: path_modifier=lambda x: Path(x).parent.absolute() if x.endswith(".json") else x (removes file and returns base folder instead)
        else:
            return "{}.{}".format(file, patterns[0].split("*.")[1]) # Append the first valid extension to file.


    def __connectStateUi(self):
        for var, ui_names in self.state_ui_connections.items():
            if isinstance(ui_names, str):
                ui_names = [ui_names]
            for ui_name in ui_names:
                ui_elem = self.ui.findChild(QtC.QObject, ui_name)
                if ui_elem is None:
                    print("ERROR: {} not found.".format(ui_name))
                else:
                    if isinstance(ui_elem, QtW.QCheckBox):
                        ui_elem.stateChanged.connect(self.__readCbx(ui_elem, var))
                    elif isinstance(ui_elem, QtW.QComboBox):
                        ui_elem.activated.connect(self.__readCbm(ui_elem, var))
                    elif isinstance(ui_elem, QtW.QSpinBox) or isinstance(ui_elem, QtW.QDoubleSpinBox):
                        ui_elem.valueChanged.connect(self.__readSbx(ui_elem, var))
                    elif isinstance(ui_elem, SNLineEdit): # IMPORTANT: keep this above base class!
                        ui_elem.editingFinished.connect(self.__readSNLed(ui_elem, var))
                    elif isinstance(ui_elem, QtW.QLineEdit):
                        ui_elem.editingFinished.connect(self.__readLed(ui_elem, var))

                    # TODO: TRIGGER THIS WITH: QtW.QApplication.instance().stateChanged.emit()
                    QtW.QApplication.instance().stateChanged.connect(self.__writeControl(ui_elem, var))

            # TODO: in derived classes also concept list, embedding list, etc. (the base widgets are handled by this, but list values need to be created
            # TODO: DYNAMIC CONTROLS CREATED AT RUNTIME CANNOT BE ATTACHED IN THIS WAY (unless they exist in the UI and are invisible...
            # TODO: MODIFY METHOD: included widgets may have a dynamic key (eg concepts.[CONCEPTID].concept_type), currently this function does not allow it, because state_ui_connection is defined before __init__

    # These methods cannot use directly lambdas, because variable names would be reassigned within the loop.
    def __readCbx(self, ui_elem, var):
        return lambda x: self._setState(var, x == Qt.Checked)
    def __readCbm(self, ui_elem, var):
        return lambda: self._setState(var, ui_elem.currentData())
    def __readSbx(self, ui_elem, var):
        return lambda x: self._setState(var, x)
    def __readSNLed(self, ui_elem, var):
        return lambda: self._setState(var, float(ui_elem.text())) # BUG: THIS DOES NOT SERIALIZE CORRECTLY!
    def __readLed(self, ui_elem, var):
        return lambda: self._setState(var, ui_elem.text())

    def __writeControl(self, ui_elem, var):
        def f():
            ui_elem.blockSignals(True)
            val = self._getState(var)
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
        return f

    def _getState(self, path):
        # Safe for dicts.
        # if self.state is not None:
        #     try:
        #         if self.mutex is not None:
        #             self.mutex.lock()
        #         ref = self.state
        #         for key in path.split("."):
        #             if isinstance(ref, dict) and key in ref:
        #                 ref = ref[key]
        #             elif isinstance(ref, list):
        #                 ref = ref[int(key)]
        #             else:
        #                 print("DEBUG: key {} not found in config".format(key))
        #                 break
        #         return ref
        #     except Exception as e:
        #         print("ERROR: {}".format(e))
        #         pass
        #     finally:
        #         if self.mutex is not None:
        #             self.mutex.unlock()
        #
        # return None

        # Unsafe for Config object.
        if self.state is not None:
            try:
                if self.mutex is not None:
                    self.mutex.lock()
                ref = self.state
                for key in path.split("."):
                    if isinstance(ref, list):
                        ref = ref[int(key)]
                    elif hasattr(ref, key):
                        ref = getattr(ref, key)
                    else:
                        print("DEBUG: key {} not found in config".format(key))
                        break
                return ref
            except Exception as e:
                print("ERROR: {}".format(e))
                pass
            finally:
                if self.mutex is not None:
                    self.mutex.unlock()

        return None

    def _setState(self, path, value):
        # Safe for dicts.
        # if self.state is not None:
        #     try:
        #         if self.mutex is not None:
        #             self.mutex.lock()
        #         ref = self.state
        #         for key in path.split(".")[:-1]:
        #             if isinstance(ref, dict) and key in ref:
        #                 ref = ref[key]
        #             elif isinstance(ref, list):
        #                 ref = ref[int(key)]
        #             else:
        #                 print("DEBUG: key {} not found in config".format(key))
        #                 break
        #         key = path.split(".")[-1]
        #         if isinstance(ref, dict) and key in ref:
        #             ref[key] = value
        #         elif isinstance(ref, list):
        #             ref[int(key)] = value
        #         else:
        #             print("DEBUG: key {} not found in config".format(key))
        #     except Exception as e:
        #         print("ERROR: {}".format(e))
        #         pass
        #     finally:
        #         if self.mutex is not None:
        #             self.mutex.unlock()

        # Unsafe, but can work directly with TrainConfig, instead of a dict version.
        #
        if self.state is not None:
            try:
                if self.mutex is not None:
                    self.mutex.lock()
                ref = self.state
                for ptr in path.split(".")[:-1]:
                    if isinstance(ref, list):
                        ref = ref[int(ptr)]
                    elif hasattr(ref, ptr):
                        ref = getattr(ref, ptr)
                if isinstance(ref, list):
                    ref[int(path.split(".")[-1])] = value
                elif hasattr(ref, path.split(".")[-1]):
                    setattr(ref, path.split(".")[-1], value)
                else:
                    print("DEBUG: key {} not found in config".format(path))
            except Exception as e:
                print("ERROR: {}".format(e))
                pass
            finally:
                if self.mutex is not None:
                    self.mutex.unlock()


    def connectFileDialog(self, tool_button, edit_box, is_dir=False, save=False, title=None, filters=None):
        assert filters is None or not is_dir, "Directories cannot be associated with filters."

        @Slot()
        def f(elem):
            diag = QtW.QFileDialog()

            if is_dir:
                dir = None
                if os.path.isdir(elem.text()):
                    dir = elem.text()
                txt = diag.getExistingDirectory(parent=None, caption=title, dir=dir)
                elem.setText(self._removeWorkingDir(txt))
            else:
                file = None
                if os.path.exists(elem.text()):
                    file = self._removeWorkingDir(elem.text())

                if save:
                    txt, flt = diag.getSaveFileName(parent=None, caption=title, dir=file, filter=filters)
                    if txt != "":
                        elem.setText(self._removeWorkingDir(self._appendExtension(txt, flt)))
                else:
                    txt, _ = diag.getOpenFileName(parent=None, caption=title, dir=file, filter=filters)
                    if txt != "":
                        elem.setText(self._removeWorkingDir(txt))

        tool_button.clicked.connect(functools.partial(f, edit_box))

    def _removeWorkingDir(self, txt):
        cwd = os.getcwd()
        if txt.startswith(cwd):
            return txt[len(cwd) + 1:] # Remove working directory and trailing slash.
        else:
            return txt

    def _appendWidget(self, list_widget, controller, self_delete_btn=False, self_clone_btn=False):
        item = QtW.QListWidgetItem(list_widget)
        item.setSizeHint(controller.ui.size())
        list_widget.addItem(item)
        list_widget.setItemWidget(item, controller.ui)

        if self_delete_btn:
            controller.ui.deleteBtn.clicked.connect(lambda: list_widget.takeItem(list_widget.row(item)))
            # TODO: DELETE ALSO CONTROLLER FROM CHILDREN!

        if self_clone_btn:
            def __clone():
                pass # TODO!
            controller.ui.cloneBtn.clicked.connect(__clone)

    def openWindow(self, controller, fixed_size=False):
        if fixed_size:
            controller.ui.setWindowFlag(Qt.WindowCloseButtonHint)
            controller.ui.setWindowFlag(Qt.WindowMaximizeButtonHint, on=False)
            controller.ui.setFixedSize(controller.ui.size())
        controller.ui.show()

    def connectUIBehavior(self):
        pass # TODO: this method handles visual behavior (eg. enable/disable lora tab dynamically)

    def connectInputValidation(self):
        pass # TODO: this method handles field validation OTHER than the automatic field validations defined in ui files.

    def loadPresets(self):
        pass