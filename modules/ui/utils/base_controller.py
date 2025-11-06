import os
import functools
import PySide6.QtWidgets as QtW
import PySide6.QtCore as QtC

from PySide6.QtCore import Slot, Qt

import re

from modules.ui.utils.sn_line_edit import SNLineEdit

from modules.ui.models.StateModel import StateModel

# TODO: CLEANUP:
# 1) Maybe it is cleaner to define callbacks always in __init__, instead of connectUIBehavior
# 2) Naming convention is all over the place (camelCase, snake_case, inconsistent visibility __method vs _method vs method)
# 3) Some callbacks are invoked as lambdas, others as self.__method() which returns a function f(). Choose one!
# 4) Finite-state machine like behavior needs to be double checked/simplified.

# Abstract controller with some utility methods.
class BaseController:
    state_ui_connections = {}

    def __init__(self, loader, ui_file, name=None, parent=None, **kwargs):
        self.loader = loader
        self.parent = parent
        self.ui = loader.load(ui_file, parentWidget=parent.ui if parent is not None else None)
        self.name = name # TODO: When necessary, derived classes will set this with QCA.translate(context, "STATIC STRING") since lupdate is a static analyzer!

        self.setup()

        self.connectUIBehavior()
        self.connectInputValidation()
        self.loadPresets()
        self._connectStateUi(self.state_ui_connections, StateModel.instance(), signal=QtW.QApplication.instance().stateChanged, **kwargs)


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


    def _connectStateUi(self, connection_dict, model, signal=None, **kwargs): # TODO: RENAME TO _connectStateUi to invoke it multiple times in child classes
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
                        ui_elem.stateChanged.connect(self.__readCbx(ui_elem, var, model))
                    elif isinstance(ui_elem, QtW.QComboBox):
                        ui_elem.activated.connect(self.__readCbm(ui_elem, var, model))
                    elif isinstance(ui_elem, QtW.QSpinBox) or isinstance(ui_elem, QtW.QDoubleSpinBox):
                        ui_elem.valueChanged.connect(self.__readSbx(ui_elem, var, model))
                    elif isinstance(ui_elem, SNLineEdit): # IMPORTANT: keep this above base class!
                        ui_elem.editingFinished.connect(self.__readSNLed(ui_elem, var, model))
                    elif isinstance(ui_elem, QtW.QLineEdit):
                        ui_elem.editingFinished.connect(self.__readLed(ui_elem, var, model))

                    if signal is not None:
                        signal.connect(functools.partial(self._writeControl,ui_elem, var, model))

    # These methods cannot use directly lambdas, because variable names would be reassigned within the loop.
    @staticmethod
    def __readCbx( ui_elem, var, model):
        return lambda x: model.setState(var, x == Qt.Checked)

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
    def _writeControl(ui_elem, var, model):
        try: # TODO: workaround: when ui_elem has been deallocated in C++, this throws a RuntimeError. I have not found a way to detect this and avoid calling the method.
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
        except RuntimeError as e:
            #print(e)
            pass




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

    def _appendWidget(self, list_widget, controller, self_delete_fn=None, self_clone_fn=None):
        item = QtW.QListWidgetItem(list_widget)
        item.setSizeHint(controller.ui.size())
        list_widget.addItem(item)
        list_widget.setItemWidget(item, controller.ui)

        if self_delete_fn is not None:
            controller.ui.deleteBtn.clicked.connect(self_delete_fn)

        if self_clone_fn is not None:
            controller.ui.cloneBtn.clicked.connect(self_clone_fn)

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