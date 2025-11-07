import sys
import os
from modules.ui.controllers.onetrainer import OnetrainerController

from modules.ui.utils.onetrainer_application import OnetrainerApplication
from PySide6.QtUiTools import QUiLoader

from PySide6.QtCore import QBasicMutex

from modules.ui.utils.sn_line_edit import SNLineEdit

from modules.util.config.TrainConfig import TrainConfig

from PySide6.QtCore import Qt

if __name__ == "__main__":
    app = OnetrainerApplication(sys.argv)
    loader = QUiLoader()
    loader.registerCustomWidget(SNLineEdit) # TODO: REMEMBER TO PROMOTE IN UI FILES! And to manually set min and max of controls (if present).

    # TODO: extract GUI agnostic functions (eg. start training, invalidate state, etc.) in modules.ui.models, grouped by logic family, not by ui element (FileModel, ConnectionModel, SamplerModel, etc.)
    # Otherwise, if the implementation remains like the current one, it becomes a Model-View architecture, instead of a Model-View-Controller and decoupling is incomplete.
    # Since the UI is relatively simple, models could be either singletons or static classes

    onetrainer = OnetrainerController(loader)

    # Invalidate ui elements after the controllers are set up, but before showing them.
    app.stateChanged.emit() # TODO: BUG! Since only QWidget values are connected to this Signal, none of the connections for UI behavior defined in connectUIBehavior() is fired. Each controller should also attach those Slots to invalid
    onetrainer.ui.show()

    sys.exit(app.exec())