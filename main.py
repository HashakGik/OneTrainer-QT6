import sys
from modules.ui.controllers.onetrainer import OnetrainerController

from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader


if __name__ == "__main__":
    app = QApplication(sys.argv)
    loader = QUiLoader()

    onetrainer = OnetrainerController(loader)

    onetrainer.ui.show()

    sys.exit(app.exec())