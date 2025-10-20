from modules.ui.utils.base_controller import BaseController

class OptimizerController(BaseController):
    def __init__(self, loader, state=None, mutex=None, parent=None):

        super().__init__(loader, "modules/ui/views/windows/optimizer.ui", state=state, mutex=mutex, name=None, parent=parent)



    def loadPresets(self):
        # TODO: fill scrollarea (grid layout) with a label->control (switched based on data type) or checkbox (2 blocks). In a modulo 2 fashion
        # TODO: Original dict does not define sensible ranges. We can add nullable min-max keys
        # Remember to add connections to original variable names (dictionary keys) to set the state

        pass