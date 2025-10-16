import os
import functools
import PySide6.QtWidgets as QtW

from PySide6.QtCore import Slot, Qt

import re

# Abstract controller with some utility methods.
class AbstractController:
    def __init__(self, loader, ui_file, state=None, name=None, parent=None):
        self.loader = loader
        self.ui = loader.load(ui_file, parentWidget=parent.ui if parent is not None else None)
        self.name = name # TODO: Derived classes will set this with QCA.translate(context, "STATIC STRING") since lupdate is a static analyzer!
        self.state = state # TODO: use it

        self.connectUIBehavior()
        self.connectInputValidation()

    def _appendExtension(self, file, filter):
        patterns = filter.split("(")[1].split(")")[0].split(", ")
        for p in patterns:
            if re.match(file, p): # If the file already has a valid extension, return it as is.
                return file

        if "*" not in patterns[0]: # The pattern is a fixed filename, returning it regardless of the user selected name.
            return patterns[0]
        else:
            return "{}.{}".format(file, patterns[0].split("*.")[1]) # Append the first valid extension to file.

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
                elem.setText(txt)
            else:
                file = None
                if os.path.exists(elem.text()):
                    file = elem.text()

                if save:
                    txt, flt = diag.getSaveFileName(parent=None, caption=title, dir=file, filter=filters)
                    elem.setText(self._appendExtension(txt, flt))
                else:
                    txt, _ = diag.getOpenFileName(parent=None, caption=title, dir=file, filter=filters)
                    elem.setText(txt)

        tool_button.clicked.connect(functools.partial(f, edit_box))

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

    def setState(self, config):
        pass

    def getState(self):
        pass

    def getDefaultState(self):
        pass # Load config file?

    def connectUIBehavior(self):
        pass # TODO: this method handles visual behavior (eg. enable/disable lora tab dynamically)

    def connectInputValidation(self):
        pass # TODO: this method handles field validation OTHER than the automatic field validations defined in ui files.
