from modules.ui.controllers.controller_utils import AbstractController


class ConceptController(AbstractController):
    def __init__(self, loader, state=None, parent=None):
        super().__init__(loader, "modules/ui/views/windows/concept.ui", state=state, name=None, parent=parent)