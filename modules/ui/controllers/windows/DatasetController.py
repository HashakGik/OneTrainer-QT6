from modules.ui.controllers.BaseController import BaseController
from PySide6.QtCore import QCoreApplication as QCA
import PySide6.QtWidgets as QtW
import PySide6.QtGui as QtG

from modules.ui.controllers.windows.CaptionController import CaptionController
from modules.ui.controllers.windows.MaskController import MaskController
from modules.ui.models.DatasetModel import DatasetModel
from modules.ui.models.MaskHistoryModel import MaskHistoryModel

from modules.util.enum.FileFilter import FileFilter
from modules.util.enum.CaptionFilter import CaptionFilter
from modules.util.enum.EditMode import EditMode

from modules.ui.utils.WorkerPool import WorkerPool

from modules.ui.utils.FigureWidget import FigureWidget, ToolType # TODO: move to enum
from modules.util.enum.MouseButton import MouseButton

from PIL import Image
import numpy as np

class DatasetController(BaseController):
    def __init__(self, loader, parent=None):
        super().__init__(loader, "modules/ui/views/windows/dataset.ui", name=None, parent=parent)

        self.theme = "dark" if QtG.QGuiApplication.styleHints().colorScheme() == QtG.Qt.ColorScheme.Dark else "light"

        # (fn, type, text, name, icon, tooltip, shortcut, spinbox_range)
        self.tools = [
            (
                self.__prevImg(), ToolType.BUTTON, "prev_btn", None, "resources/icons/buttons/{}/arrow-left.svg".format(self.theme),
             QCA.translate("toolbar_item", "Previous image (Left Arrow)"), "Left", None
            ),
            (
                self.__nextImg(), ToolType.BUTTON, "next_btn", None, "resources/icons/buttons/{}/arrow-right.svg".format(self.theme),
             QCA.translate("toolbar_item", "Next image (Right Arrow)"), "Right", None
            ),
            (None, ToolType.SEPARATOR, None, None, None, None, None, None),
            (
                self.__toggleMaskEdit(), ToolType.CHECKABLE_BUTTON, "draw_btn", None, "resources/icons/buttons/{}/brush.svg".format(self.theme),
                QCA.translate("toolbar_item", "Draw (Left Click) or Erase (Right Click) mask (CTRL+E)"), "Ctrl+E", None
            ),
            (
                self.__toggleMaskFill(), ToolType.CHECKABLE_BUTTON, "fill_btn", None,
                "resources/icons/buttons/{}/paint-bucket.svg".format(self.theme),
                QCA.translate("toolbar_item",
                              "Fill (Left Click) or Erase-fill (Right Click) mask (CTRL+F)"), "Ctrl+F", None
            ),
            (
                self.__setBrushSize(), ToolType.SPINBOX, "brush_sbx", QCA.translate("toolbar_item", "Brush size"), None,
                              QCA.translate("toolbar_item", "Brush size (Mouse Wheel Up/Down)"), None, (1, 256.0, 1.0) # TODO: CHECK RANGE. SHORTCUT.
            ),
            (
                self.__setAlpha(), ToolType.SPINBOX, "alpha_sbx", QCA.translate("toolbar_item", "Mask opacity"), None,
                QCA.translate("toolbar_item", "Mask opacity for preview"), None, (0.05, 1.0, 0.05)
            ),
            (None, ToolType.SEPARATOR, None, None, None, None, None, None),
            (
                self.__clearAll(), ToolType.BUTTON, "clear_btn", QCA.translate("toolbar_item", "Clear All"), None,
                              QCA.translate("toolbar_item", "Clear mask and caption (Del)"), "Del", None
            ),
            (
                self.__resetMask(), ToolType.BUTTON, "reset_btn", QCA.translate("toolbar_item", "Reset Mask"), None,
                              QCA.translate("toolbar_item", "Reset mask (CTRL+R, or Middle Click)"), "Ctrl+R", None
            ),
            (None, ToolType.SEPARATOR, None, None, None, None, None, None),
            (
                self.__saveMask(), ToolType.BUTTON, "save_btn", None, "resources/icons/buttons/{}/save.svg".format(self.theme),
                              QCA.translate("toolbar_item", "Save mask (CTRL+S)"), "Ctrl+S", None
            ),
            (
                self.__undo(), ToolType.BUTTON, "undo_btn", None, "resources/icons/buttons/{}/undo.svg".format(self.theme),
                QCA.translate("toolbar_item", "Undo (CTRL+Z)"), "Ctrl+Z", None
            ),
            (
                self.__redo(), ToolType.BUTTON, "redo_btn", None, "resources/icons/buttons/{}/redo.svg".format(self.theme),
                              QCA.translate("toolbar_item", "Redo (CTRL+Y)"), "Ctrl+Y", None
            ),
            (None, ToolType.SEPARATOR, None, None, None, None, None, None),
            (
                self.__deleteSample(), ToolType.BUTTON, "delete_btn", None, "resources/icons/buttons/{}/trash-2.svg".format(self.theme),
                QCA.translate("toolbar_item", "Delete image and caption (CTRL+Del)"), "Ctrl+Del", None
            ),
        ]


        self.canvas = FigureWidget(parent=self.ui, width=7, height=5, zoom_tools=True, other_tools=self.tools, emit_clicked=True, emit_moved=True, emit_wheel=True, emit_released=True, use_data_coordinates=True)
        self.ax = self.canvas.figure.subplots()

        self.ui.canvasLay.addWidget(self.canvas.toolbar)
        self.ui.canvasLay.addWidget(self.canvas)

        self.connect(self.canvas.clicked, self.__onClicked())
        self.connect(self.canvas.released, self.__onReleased())
        self.connect(self.canvas.moved, self.__onMoved())
        self.connect(self.canvas.wheelUp, self.__onWheelUp())
        self.connect(self.canvas.wheelDown, self.__onWheelDown())

        # TODO: new windows: Image tools, Bulk Caption edit

        """
        DRAWING:
        https://stackoverflow.com/questions/76571540/how-do-i-add-figurecanvasqtagg-in-a-pyqt-layout

        https://stackoverflow.com/questions/72242466/how-to-draw-on-an-image-tkinter-canvas-pil

        """


        self.help_window = QtW.QMessageBox(QtW.QMessageBox.Icon.NoIcon, QCA.translate("dialog_window", "Dataset Tools Help"),
                                 QCA.translate("help_dataset", """
Keyboard shortcuts when focusing on the prompt input field:
Up arrow: previous image
Down arrow: next image
Return: save
Ctrl+M: only show the mask
Ctrl+D: draw mask editing mode
Ctrl+F: fill mask editing mode

When editing masks:
Left click: add mask
Right click: remove mask
Mouse wheel: increase or decrease brush size
"""))
        self.help_window.setModal(False) # TODO: Change to openAlert. Change content to reflect new controls.

        self.mask_window = MaskController(loader, parent=self)
        self.caption_window = CaptionController(loader, parent=self)

        
        self.leafWidgets = {}
        self.num_files = 0
        self.current_index = 0
        self.alpha = 0.05 # TODO: read/write from toolbar
        self.brush = 1.0 # TODO read/write from toolbar
        self.current_tool = EditMode.NONE # TODO: reset every time a new image is loaded?
        self.ax = self.canvas.figure.subplots()
        self.im = None

    def __openDataset(self):
        def f():
            diag = QtW.QFileDialog()
            dir = diag.getExistingDirectory(parent=None, caption=QCA.translate("dialog_window", "Open Dataset directory"), dir=DatasetModel.instance().getState("path"))

            worker = WorkerPool.instance().runNamed(self.__scan(), name="open_dataset", dir=dir)
            worker.connect(finished_fn=self.__updateDataset())

        return f

    def __scan(self):
        def f(dir):
            DatasetModel.instance().setState("path", dir)
            DatasetModel.instance().scan()
        return f

    def __updateDataset(self):
        def f():
            files = DatasetModel.instance().getFilteredFiles()
            self.current_index = 0
            self.num_files = len(files)
            if self.num_files == 0:
                self.ui.numFilesLbl.setText(QCA.translate("dataset_window", "No image found"))
            else:
                self.ui.numFilesLbl.setText(QCA.translate("dataset_window", "Dataset loaded"))

            file_tree = {}
            for i, file in enumerate(files):
                self.__buildTree(file, file_tree, i)

            self.ui.fileTreeWdg.clear()
            self.leafWidgets = {}
            self.__drawTree(self.ui.fileTreeWdg, file_tree)

        return f

    def __prevImg(self):
        def f():
            if self.num_files > 0:
                # TODO: if mask or caption is changed, ask for save (Yes: save and move to next, No: discard and move to next, Cancel: do not move and undo gui selection
                self.current_index = (self.current_index + self.num_files - 1) % self.num_files
                self.ui.fileTreeWdg.setCurrentItem(self.leafWidgets[self.current_index])
        return f

    def __nextImg(self):
        def f():
            if self.num_files > 0:
                # TODO: if mask or caption is changed, ask for save (Yes: save and move to next, No: discard and move to next, Cancel: do not move and undo gui selection
                self.current_index = (self.current_index + 1) % self.num_files
                self.ui.fileTreeWdg.setCurrentItem(self.leafWidgets[self.current_index])
        return f

    def __toggleMaskEdit(self):
        def f(): # TODO: take bool param?
            if self.current_tool == EditMode.DRAW:
                self.current_tool = EditMode.NONE
            else:
                self.current_tool = EditMode.DRAW
            # TODO: disable pan/zoom and checked
        return f

    def __toggleMaskFill(self):
        def f(): # TODO: take bool param?
            if self.current_tool == EditMode.FILL:
                self.current_tool = EditMode.NONE
            else:
                self.current_tool = EditMode.FILL
            # TODO: disable pan/zoom and checked
        return f

    def __setBrushSize(self):
        def f(val):
            self.brush = val
        return f

    def __setAlpha(self):
        def f(val):
            self.alpha = val

            self.__updateCanvas()
        return f

    def __clearAll(self):
        def f():
            pass  # TODO: ASK FOR CONFIRMATION.

            self.__updateCanvas()
        return f

    def __resetMask(self):
        def f():
            pass # TODO: Push empty mask on history buffer

            self.__updateCanvas()
        return f

    def __undo(self):
        def f():
            MaskHistoryModel.instance().undo()

            self.__updateCanvas()
        return f

    def __redo(self):
        def f():
            MaskHistoryModel.instance().redo()

            self.__updateCanvas()
        return f

    def __saveMask(self):
        def f():
            pass # TODO: Do we also need a __saveCaption?
        return f

    def __deleteSample(self):
        def f():
            # TODO: When deleting the image, also update the model (and trigger a tree update)!
            pass
        return f

    def __buildTree(self, fullname, tree, idx, name=None):
        if name is None:
            name = fullname
        path = name.split("/")
        if len(path) == 1:
            tree[path[0]] = (idx, fullname)
        elif len(path) > 1:
            if path[0] not in tree:
                tree[path[0]] = {}
            self.__buildTree(fullname, tree[path[0]], idx, "/".join(path[1:]))

    def __drawTree(self, parent, tree):
        for k in sorted(tree.keys(), key=lambda x: DatasetModel.natural_sort_key(x)):
            v = tree[k]
            wdg = QtW.QTreeWidgetItem(parent, [k])
            if isinstance(v, dict):
                wdg.setIcon(0, QtG.QIcon("resources/icons/buttons/{}/folder-open.svg".format(self.theme)))
                wdg.fullpath = None
                wdg.idx = None
                self.__drawTree(wdg, v)
            else:
                # TODO: MAYBE ADD ICON TO SHOW WHICH IMAGES HAVE CAPTIONS AND WHICH HAVE MASKS? (change "files" to list of (img, mask, caption) in model)
                # wdg.setIcon(0, QtG.QIcon("resources/icons/buttons/{}/???.svg".format(self.theme)))
                # setTooltip to tell whether captions and masks exist
                #
                # file-x-corner -> img only ("No caption or mask found")
                # file-scan -> img + mask ("Missing caption")
                # file-minus-corner -> img + caption ("Missing mask")
                # file-check-corner -> img + mask + caption ("Caption and mask available")

                wdg.fullpath = v[1]
                wdg.idx = v[0]
                self.leafWidgets[v[0]] = wdg


    def __selectFile(self):
        def f():
            selected_wdg = self.ui.fileTreeWdg.selectedItems()
            if len(selected_wdg) > 0:
                path = selected_wdg[0].fullpath
                idx = selected_wdg[0].idx
                if path is not None:
                    if self.num_files > 0:
                        if idx is not None:
                            self.current_index = idx
                            self.ui.numFilesLbl.setText("{}/{}".format(self.current_index + 1, self.num_files))
    
                            # TODO: use DatasetModel.instance().getState("files")[self.current_index] to load image and caption (OR SAVE CURRENT PATH LOCALLY FROM path when not None)
                            self.image, mask, self.original_caption = DatasetModel.instance().getSample(path)
                            # TODO: USE IMAGE, MASK, CAPTION?
                            if self.original_caption is not None:
                                self.ui.captionTed.setPlainText(self.original_caption) # TODO: WHEN SAVING CHECK: file exists and caption has changed, file does not exist and caption is not empty (create file), file exists and caption ted is empty (delete file)
                            # self.canvas.drawImage(image, self.ax, alpha=1.0, layer=0)
                            # if mask is not None:
                            #     self.canvas.drawImage(mask, self.ax, alpha=self.alpha, layer=1) # TODO: dynamic alpha based on toolbar

                            if mask is None:
                                mask = Image.new("L", self.image.size, 1)

                            MaskHistoryModel.instance().loadMask(np.asarray(mask))
                            self.im = self.ax.imshow(self.image)

                            self.__updateCanvas()

        return f

    def __updateCanvas(self):
        if self.im is not None:
            mask = np.clip(MaskHistoryModel.instance().getState("current_mask")[..., np.newaxis].astype(float), 1 - self.alpha, 1)
            self.im.set_data((np.asarray(self.image) * mask).astype(np.uint8))

            self.canvas.draw_idle()

    def __browse(self): # TODO: MOVE IN BASE CONTROLLER ALONG WITH OPEN_URL, ETC. (TO AVOID CREATING A MISC MODEL)?
        def f():
            pass # We might consider adding a dependency to: https://pypi.org/project/show-in-file-manager/
        return f

    def __onClicked(self):
        def f(btn, x, y):
            if self.current_tool == EditMode.FILL:
                if btn == MouseButton.LEFT:
                    MaskHistoryModel.instance().fill(x, y, 0)
                elif btn == MouseButton.RIGHT:
                    MaskHistoryModel.instance().fill(x, y, 1)
            else:
                if btn == MouseButton.MIDDLE:
                    MaskHistoryModel.instance().reset()

            self.__updateCanvas()
        return f

    def __onReleased(self):
        def f(btn, x, y):
            MaskHistoryModel.instance().commit()

            self.__updateCanvas()
        return f

    def __onWheelUp(self):
        def f():
            wdg = self.canvas.toolbar.findChild(QtW.QDoubleSpinBox, "brush_sbx")
            new_val = wdg.value() + wdg.singleStep()
            wdg.setValue(new_val) # This will emit valueChanged, which is connected to self.__setBrushSize()
        return f

    def __onWheelDown(self):
        def f():
            wdg = self.canvas.toolbar.findChild(QtW.QDoubleSpinBox, "brush_sbx")
            new_val = wdg.value() - wdg.singleStep()
            wdg.setValue(new_val)
        return f

    def __onMoved(self):
        def f(btn, x0, y0, x1, y1):
            if self.current_tool == EditMode.DRAW and x0 >= 0 and y0 >= 0 and x1 >= 0 and y1 >= 0:
                if btn == MouseButton.LEFT:
                    MaskHistoryModel.instance().paintStroke(x0, y0, x1, y1, int(self.brush), 0, commit=False)  # Draw stroke 0 from x0,y0 to x1,y1
                    self.__updateCanvas()
                elif btn == MouseButton.RIGHT:
                    MaskHistoryModel.instance().paintStroke(x0, y0, x1, y1, int(self.brush), 1, commit=False)
                    self.__updateCanvas()


            else:
                pass # Do nothing?


        return f

    def _connectUIBehavior(self):
        state_ui_connections = {
            "include_subdirectories": "includeSubdirCbx",
            "file_filter": "fileFilterLed",
            "file_filter_mode": "fileFilterCmb",
            "caption_filter": "captionFilterLed",
            "caption_filter_mode": "captionFilterCmb",
        }

        self._connectStateUi(state_ui_connections, DatasetModel.instance(), signal=None, update_after_connect=True)

        self.connect(self.ui.openBtn.clicked, self.__openDataset())
        self.connect(self.ui.generateMaskBtn.clicked, lambda: self.openWindow(self.mask_window, fixed_size=True))
        self.connect(self.ui.generateCaptionsBtn.clicked, lambda: self.openWindow(self.caption_window, fixed_size=True))
        self.connect(self.ui.helpBtn.clicked, lambda: self.help_window.show())
        self.connect(self.ui.browseBtn.clicked, self.__browse())

        self.connect(self.ui.fileTreeWdg.itemSelectionChanged, self.__selectFile())

        self.connect(self.ui.fileFilterLed.editingFinished, self.__updateDataset())
        self.connect(self.ui.fileFilterCmb.activated, self.__updateDataset())
        self.connect(self.ui.captionFilterLed.editingFinished, self.__updateDataset())
        self.connect(self.ui.captionFilterCmb.activated, self.__updateDataset())


    def _loadPresets(self):
        for e in FileFilter.enabled_values():
            self.ui.fileFilterCmb.addItem(e.pretty_print(), userData=e)

        for e in CaptionFilter.enabled_values():
            self.ui.captionFilterCmb.addItem(e.pretty_print(), userData=e)