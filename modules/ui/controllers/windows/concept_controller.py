from modules.ui.utils.base_controller import BaseController

from modules.ui.utils.figure_widget import FigureWidget

from PySide6.QtCore import QCoreApplication as QCA
import PySide6.QtWidgets as QtW

from modules.util.enum.BalancingStrategy import BalancingStrategy
from modules.util.enum.ConceptType import ConceptType
from modules.util.enum.TrainingMethod import TrainingMethod

from modules.util.enum.DropoutMode import DropoutMode
from modules.util.enum.PromptSource import PromptSource
from modules.util.enum.SpecialDropoutTags import SpecialDropoutTags

from modules.ui.models.ConceptModel import ConceptModel


class ConceptController(BaseController):
    def __init__(self, loader, parent=None):
        super().__init__(loader, "modules/ui/views/windows/concept.ui", name=None, parent=parent)

        self.idx = 0

        #self.canvas = FigureCanvas(Figure(figsize=(8, 3))) # TODO: refactor magic numbers. Possibly suggest a size in pixel for default rendering.
        # self.canvas = FigureWidget(parent=self.ui, zoom_tools=True, navigation_tools=True, edit_tools=True)
        # self.ui.histogramLay.addWidget(self.canvas.toolbar) # Matplotlib toolbar, in case we want the user to zoom in. TODO: add only relevant buttons (zoom, move, lin-log scale, etc.)
        # self.ui.histogramLay.addWidget(self.canvas)
        #
        # x = [1, 2, 3, 4, 5]
        # y = [2, 4, 6, 8, 10]
        # ax = self.canvas.figure.subplots()
        # ax.plot((x,y))


    # TODO: create CanvasWidget (subclass of FigureCanvas) to handle default color picking, etc., here just pass the data. Maybe even the entire canvas could be a class drawable=True/False
    #       modify ui replacing layout with QWidget promoted to CanvasWidget

    # TODO: FOR CONCEPT BUTTON DRAWING USE THIS INSTEAD: https://stackoverflow.com/questions/34697559/pil-image-to-qpixmap-conversion-issue

    """
    DRAWING:
    https://stackoverflow.com/questions/76571540/how-do-i-add-figurecanvasqtagg-in-a-pyqt-layout
    
    https://stackoverflow.com/questions/72242466/how-to-draw-on-an-image-tkinter-canvas-pil
    
    https://stackoverflow.com/questions/15721094/detecting-mouse-event-in-an-image-with-matplotlib
    https://matplotlib.org/3.2.2/users/event_handling.html#mouse-enter-and-leave
    https://scipy-cookbook.readthedocs.io/items/Matplotlib_Animations.html
    
    IDEA: 
    1)create canvas associated with PIL/numpy bitmask
    2)use mouse events to determine a start and end position
    3)draw a line on the bitmask
    4)bitblit the line on the canvas efficiently
    5)Use the bitmask for business logic
    
    BONUS: use matplotlib toolbox for draw/delete, instead of buttons + shortcuts
    https://matplotlib.org/stable/gallery/user_interfaces/toolmanager_sgskip.html 
    
    """

    def __enablePromptSource(self, _):
        if self.ui.promptSourceCmb.currentData() != "concept": # Replace with "PromptSource.CONCEPT" when ConceptConfig will accept enum instead of string.
            self.ui.promptSourceLed.setEnabled(False)
            self.ui.promptSourceBtn.setEnabled(False)
        else:
            self.ui.promptSourceLed.setEnabled(True)
            self.ui.promptSourceBtn.setEnabled(True)

    def __updateConcept(self):
        def f(idx):
            self.idx = idx

            # General tab.
            self._writeControl(self.ui.nameLed, "{}.name".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.enabledCbx, "{}.enabled".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.conceptTypeCmb, "{}.type".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.pathLed, "{}.path".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.promptSourceCmb, "{}.text.prompt_source".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.promptSourceLed, "{}.text.prompt_path".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.includeSubdirectoriesCbx, "{}.include_subdirectories".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.imageVariationsSbx, "{}.image_variations".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.textVariationsSbx, "{}.text_variations".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.balancingSbx, "{}.balancing".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.balancingCmb, "{}.balancing_strategy".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.lossWeightSbx, "{}.loss_weight".format(idx), ConceptModel.instance())

            # Image augmentation tab.
            self._writeControl(self.ui.rndJitterCbx, "{}.image.enable_crop_jitter".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.rndFlipCbx, "{}.image.enable_random_flip".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.fixFlipCbx, "{}.image.enable_fixed_flip".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.rndRotationCbx, "{}.image.enable_random_rotate".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.fixRotationCbx, "{}.image.enable_fixed_rotate".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.rotationSbx, "{}.image.random_rotate_max_angle".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.rndBrightnessCbx, "{}.image.enable_random_brightness".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.fixBrightnessCbx, "{}.image.enable_fixed_brightness".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.brightnessSbx, "{}.image.random_brightness_max_strength".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.rndContrastCbx, "{}.image.enable_random_contrast".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.fixContrastCbx, "{}.image.enable_fixed_contrast".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.contrastSbx, "{}.image.random_contrast_max_strength".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.rndSaturationCbx, "{}.image.enable_random_saturation".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.fixSaturationCbx, "{}.image.enable_fixed_saturation".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.saturationSbx, "{}.image.random_saturation_max_strength".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.rndHueCbx, "{}.image.enable_random_hue".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.fixHueCbx, "{}.image.enable_fixed_hue".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.hueSbx, "{}.image.random_hue_max_strength".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.fixResolutionOverrideCbx, "{}.image.enable_resolution_override".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.resolutionOverrideSbx, "{}.image.resolution_override".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.rndCircularMaskCbx, "{}.image.enable_random_circular_mask_shrink".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.rndRotateCropCbx, "{}.image.enable_random_mask_rotate_crop".format(idx), ConceptModel.instance())

            # Text augmentation tab.
            self._writeControl(self.ui.tagShufflingCbx, "{}.text.enable_tag_shuffling".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.tagDelimiterLed, "{}.text.tag_delimiter".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.keepTagCountSbx, "{}.text.keep_tags_count".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.tagDropoutCbx, "{}.text.tag_dropout_enable".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.dropoutModeCmb, "{}.text.tag_dropout_mode".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.dropoutProbabilitySbx, "{}.text.tag_dropout_probability".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.specialDropoutTagsCmb, "{}.text.tag_dropout_special_tags_mode".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.specialDropoutTagsLed, "{}.text.tag_dropout_special_tags".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.specialTagsRegexCbx, "{}.text.tag_dropout_special_tags_regex".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.randomizeCapitalizationCbx, "{}.text.caps_randomize_enable".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.capitalizationProbabilitySbx, "{}.text.caps_randomize_probability".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.capitalizationModeLed, "{}.text.caps_randomize_mode".format(idx), ConceptModel.instance())
            self._writeControl(self.ui.forceLowercaseCbx, "{}.text.caps_randomize_lowercase".format(idx), ConceptModel.instance())

            # Statistics tab.
            # TODO: populate basicStatListWidget, advancedStatListWidget and histogramLay using "{}.concept_stats"
            # {}.concept_stats is a dictionary:
            # Histogram: concept_stats["aspect_buckets"]
            # Base stats: file_size (convert to MB), image_count, mask_count, caption_count, subcaption_count, directory_count, processing_time


            pass
        return f

    def __saveConcept(self):
        def f():
            # General tab.
            ConceptModel.instance().setState("{}.name".format(self.idx), self.ui.nameLed.text())
            ConceptModel.instance().setState("{}.enabled".format(self.idx), self.ui.enabledCbx.isChecked())
            ConceptModel.instance().setState("{}.type".format(self.idx), self.ui.conceptTypeCmb.currentData())
            ConceptModel.instance().setState("{}.path".format(self.idx), self.ui.pathLed.text())
            ConceptModel.instance().setState("{}.text.prompt_source".format(self.idx), self.ui.promptSourceCmb.currentData())
            ConceptModel.instance().setState("{}.text.prompt_path".format(self.idx), self.ui.promptSourceLed.text())
            ConceptModel.instance().setState("{}.include_subdirectories".format(self.idx), self.ui.includeSubdirectoriesCbx.isChecked())
            ConceptModel.instance().setState("{}.image_variations".format(self.idx), self.ui.imageVariationsSbx.value())
            ConceptModel.instance().setState("{}.text_variations".format(self.idx), self.ui.textVariationsSbx.value())
            ConceptModel.instance().setState("{}.balancing".format(self.idx), self.ui.balancingSbx.value())
            ConceptModel.instance().setState("{}.balancing_strategy".format(self.idx), self.ui.balancingCmb.currentData())
            ConceptModel.instance().setState("{}.loss_weight".format(self.idx), self.ui.lossWeightSbx.value())

            # Image augmentation tab.
            ConceptModel.instance().setState("{}.image.enable_crop_jitter".format(self.idx), self.ui.rndJitterCbx.isChecked())
            ConceptModel.instance().setState("{}.image.enable_random_flip".format(self.idx), self.ui.rndFlipCbx.isChecked())
            ConceptModel.instance().setState("{}.image.enable_fixed_flip".format(self.idx), self.ui.fixFlipCbx.isChecked())
            ConceptModel.instance().setState("{}.image.enable_random_rotate".format(self.idx), self.ui.rndRotationCbx.isChecked())
            ConceptModel.instance().setState("{}.image.enable_fixed_rotate".format(self.idx), self.ui.fixRotationCbx.isChecked())
            ConceptModel.instance().setState("{}.image.random_rotate_max_angle".format(self.idx), self.ui.rotationSbx.value())
            ConceptModel.instance().setState("{}.image.enable_random_brightness".format(self.idx), self.ui.rndBrightnessCbx.isChecked())
            ConceptModel.instance().setState("{}.image.enable_fixed_brightness".format(self.idx), self.ui.fixBrightnessCbx.isChecked())
            ConceptModel.instance().setState("{}.image.random_brightness_max_strength".format(self.idx), self.ui.brightnessSbx.value())
            ConceptModel.instance().setState("{}.image.enable_random_contrast".format(self.idx), self.ui.rndContrastCbx.isChecked())
            ConceptModel.instance().setState("{}.image.enable_fixed_contrast".format(self.idx), self.ui.fixContrastCbx.isChecked())
            ConceptModel.instance().setState("{}.image.random_contrast_max_strength".format(self.idx), self.ui.contrastSbx.value())
            ConceptModel.instance().setState("{}.image.enable_random_saturation".format(self.idx), self.ui.rndSaturationCbx.isChecked())
            ConceptModel.instance().setState("{}.image.enable_fixed_saturation".format(self.idx), self.ui.fixSaturationCbx.isChecked())
            ConceptModel.instance().setState("{}.image.random_saturation_max_strength".format(self.idx), self.ui.saturationSbx.value())
            ConceptModel.instance().setState("{}.image.enable_random_hue".format(self.idx), self.ui.rndHueCbx.isChecked())
            ConceptModel.instance().setState("{}.image.enable_fixed_hue".format(self.idx), self.ui.fixHueCbx.isChecked())
            ConceptModel.instance().setState("{}.image.random_hue_max_strength".format(self.idx), self.ui.hueSbx.value())
            ConceptModel.instance().setState("{}.image.enable_resolution_override".format(self.idx), self.ui.fixResolutionOverrideCbx.isChecked())
            ConceptModel.instance().setState("{}.image.resolution_override".format(self.idx), self.ui.resolutionOverrideSbx.value())
            ConceptModel.instance().setState("{}.image.enable_random_circular_mask_shrink".format(self.idx), self.ui.rndCircularMaskCbx.isChecked())
            ConceptModel.instance().setState("{}.image.enable_random_mask_rotate_crop".format(self.idx), self.ui.rndRotateCropCbx.isChecked())


            # Text augmentation tab.
            ConceptModel.instance().setState("{}.text.enable_tag_shuffling".format(self.idx), self.ui.tagShufflingCbx.isChecked())
            ConceptModel.instance().setState("{}.text.tag_delimiter".format(self.idx), self.ui.tagDelimiterLed.text())
            ConceptModel.instance().setState("{}.text.keep_tags_count".format(self.idx), self.ui.keepTagCountSbx.value())
            ConceptModel.instance().setState("{}.text.tag_dropout_enable".format(self.idx), self.ui.tagDropoutCbx.isChecked())
            ConceptModel.instance().setState("{}.text.tag_dropout_mode".format(self.idx), self.ui.dropoutModeCmb.currentData())
            ConceptModel.instance().setState("{}.text.tag_dropout_probability".format(self.idx), self.ui.dropoutProbabilitySbx.value())
            ConceptModel.instance().setState("{}.text.tag_dropout_special_tags_mode".format(self.idx), self.ui.specialDropoutTagsCmb.currentData())
            ConceptModel.instance().setState("{}.text.tag_dropout_special_tags".format(self.idx), self.ui.specialDropoutTagsLed.text())
            ConceptModel.instance().setState("{}.text.tag_dropout_special_tags_regex".format(self.idx), self.ui.specialTagsRegexCbx.isChecked())
            ConceptModel.instance().setState("{}.text.caps_randomize_enable".format(self.idx), self.ui.randomizeCapitalizationCbx.isChecked())
            ConceptModel.instance().setState("{}.text.caps_randomize_probability".format(self.idx), self.ui.capitalizationProbabilitySbx.value())
            ConceptModel.instance().setState("{}.text.caps_randomize_mode".format(self.idx), self.ui.capitalizationModeLed.text())
            ConceptModel.instance().setState("{}.text.caps_randomize_lowercase".format(self.idx), self.ui.forceLowercaseCbx.isChecked())

            # No need to store statistics, as they are handled directly by the model.
            QtW.QApplication.instance().conceptsChanged.emit()
            self.ui.hide()
        return f

    def connectUIBehavior(self):
        self.connectFileDialog(self.ui.pathBtn, self.ui.pathLed, is_dir=True, title=QCA.translate("dialog_window", "Open Dataset directory"))
        self.connectFileDialog(self.ui.promptSourceBtn, self.ui.promptSourceLed, is_dir=False,
                               title=QCA.translate("dialog_window", "Open Prompt Source"),
                               filters=QCA.translate("filetype_filters",
                                                     "Text (*.txt)"))

        self.connect(QtW.QApplication.instance().openConcept, self.__updateConcept())
        self.connect(self.ui.okBtn.clicked, self.__saveConcept())

        # TODO: showAugmentationsCbx, update preview, <, >, filenameLbl, promptTed


    def connectInputValidation(self):
        self.connect(self.ui.promptSourceCmb.activated, self.__enablePromptSource)

    def loadPresets(self):
        for e in PromptSource.enabled_values():
            self.ui.promptSourceCmb.addItem(e.pretty_print(), userData=str(e)) # ConceptConfig serializes string, not enum

        for e in DropoutMode.enabled_values():
            self.ui.dropoutModeCmb.addItem(e.pretty_print(), userData=str(e)) # ConceptConfig serializes string, not enum

        for e in SpecialDropoutTags.enabled_values():
            self.ui.specialDropoutTagsCmb.addItem(e.pretty_print(), userData=str(e)) # ConceptConfig serializes string, not enum

        for e in BalancingStrategy.enabled_values():
            self.ui.balancingCmb.addItem(e.pretty_print(), userData=e)

        # TODO: this always allows Prior Validation concepts, even when LORA is not selected. (The behavior is the same as original OneTrainer, delegating checks to non-ui methods)
        for e in ConceptType.enabled_values(context="prior_pred_enabled"):
            self.ui.conceptTypeCmb.addItem(e.pretty_print(), userData=e)