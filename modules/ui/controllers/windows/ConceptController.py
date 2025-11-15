from modules.ui.controllers.BaseController import BaseController

from modules.ui.utils.FigureWidget import FigureWidget
from modules.ui.utils.WorkerThread import WorkerThread # TODO: replace with WorkerPool

from PySide6.QtCore import QCoreApplication as QCA
import PySide6.QtWidgets as QtW

from PySide6.QtCore import QTimer

from modules.util.enum.BalancingStrategy import BalancingStrategy
from modules.util.enum.ConceptType import ConceptType


from modules.util.enum.DropoutMode import DropoutMode
from modules.util.enum.PromptSource import PromptSource
from modules.util.enum.SpecialDropoutTags import SpecialDropoutTags

from modules.ui.models.ConceptModel import ConceptModel

import PySide6.QtGui as QtGui
from PIL.ImageQt import ImageQt
from matplotlib import pyplot as plt


class ConceptController(BaseController):
    def __init__(self, loader, parent=None):
        super().__init__(loader, "modules/ui/views/windows/concept.ui", name=None, parent=parent)

        self.idx = 0
        self.file_index = 0
        self.timer = QTimer()
        self.worker = WorkerThread(self.__scanConcept(), on_end_fn=self.__conceptScannedCallback(), abort_fn=self.__abortScan())
        # self.worker.start() # TODO: either solve deadlock on advanced scan, or restore original implementation.

        self.connect(self.timer.timeout, self.__updateTitle())
        self.connect(QtW.QApplication.instance().openConcept, self.__enableTimer())
        self.connect(QtW.QApplication.instance().openConcept, self.__updateImage())

        self.dynamic_state_ui_connections = {
            # General tab.
            "{idx}.enabled": "enabledCbx",
            "{idx}.type": "conceptTypeCmb",
            "{idx}.path": "pathLed",
            "{idx}.text.prompt_source": "promptSourceCmb",
            "{idx}.text.prompt_path": "promptSourceLed",
            "{idx}.include_subdirectories": "includeSubdirectoriesCbx",
            "{idx}.image_variations": "imageVariationsSbx",
            "{idx}.text_variations": "textVariationsSbx",
            "{idx}.balancing": "balancingSbx",
            "{idx}.balancing_strategy": "balancingCmb",
            "{idx}.loss_weight": "lossWeightSbx",
            # Image augmentation tab.
            "{idx}.image.enable_crop_jitter": "rndJitterCbx",
            "{idx}.image.enable_random_flip": "rndFlipCbx",
            "{idx}.image.enable_fixed_flip": "fixFlipCbx",
            "{idx}.image.enable_random_rotate": "rndRotationCbx",
            "{idx}.image.enable_fixed_rotate": "fixRotationCbx",
            "{idx}.image.random_rotate_max_angle": "rotationSbx",
            "{idx}.image.enable_random_brightness": "rndBrightnessCbx",
            "{idx}.image.enable_fixed_brightness": "fixBrightnessCbx",
            "{idx}.image.random_brightness_max_strength": "brightnessSbx",
            "{idx}.image.enable_random_contrast": "rndContrastCbx",
            "{idx}.image.enable_fixed_contrast": "fixContrastCbx",
            "{idx}.image.random_contrast_max_strength": "contrastSbx",
            "{idx}.image.enable_random_saturation": "rndSaturationCbx",
            "{idx}.image.enable_fixed_saturation": "fixSaturationCbx",
            "{idx}.image.random_saturation_max_strength": "saturationSbx",
            "{idx}.image.enable_random_hue": "rndHueCbx",
            "{idx}.image.enable_fixed_hue": "fixHueCbx",
            "{idx}.image.random_hue_max_strength": "hueSbx",
            "{idx}.image.enable_resolution_override": "fixResolutionOverrideCbx",
            "{idx}.image.resolution_override": "resolutionOverrideSbx",
            "{idx}.image.enable_random_circular_mask_shrink": "rndCircularMaskCbx",
            "{idx}.image.enable_random_mask_rotate_crop": "rndRotateCropCbx",
            # Text augmentation tab.
            "{idx}.text.enable_tag_shuffling": "tagShufflingCbx",
            "{idx}.text.tag_delimiter": "tagDelimiterLed",
            "{idx}.text.keep_tags_count": "keepTagCountSbx",
            "{idx}.text.tag_dropout_enable": "tagDropoutCbx",
            "{idx}.text.tag_dropout_mode": "dropoutModeCmb",
            "{idx}.text.tag_dropout_probability": "dropoutProbabilitySbx",
            "{idx}.text.tag_dropout_special_tags_mode": "specialDropoutTagsCmb",
            "{idx}.text.tag_dropout_special_tags": "specialDropoutTagsLed",
            "{idx}.text.tag_dropout_special_tags_regex": "specialTagsRegexCbx",
            "{idx}.text.caps_randomize_enable": "randomizeCapitalizationCbx",
            "{idx}.text.caps_randomize_probability": "capitalizationProbabilitySbx",
            "{idx}.text.caps_randomize_mode": "capitalizationModeLed",
            "{idx}.text.caps_randomize_lowercase": "forceLowercaseCbx",
        }

        self.connect(QtW.QApplication.instance().openConcept, self.__reconnectControls())

        # TODO: TKinter implementation does a basic scan automatically when the window is created, then retries an advanced one if basic took < 0.1s
        # A more robust approach would be to have a queuing mechanism:
        # On preset change: enqueue every concept's path that is not associated with statistics
        # On okBtn clicked: if new path != old path -> enqueue current concept's path
        # On Update Basic/Advanced Statistics: add current concept to top of queue, instead of bottom
        # The queue is processed concurrently while the application is running (the thread uses a QSemaphore on the list to sleep as long as it is empty)
        # On enqueue (by main thread) Semaphore.release(1), Before every dequeue Semaphore.acquire(1) (by scanner thread)

        plt.set_loglevel('WARNING')  # suppress errors about data type in bar chart

        self.canvas = FigureWidget(parent=self.ui, width=7, height=3, zoom_tools=True)
        self.bucket_ax = self.canvas.figure.subplots()
        self.ui.histogramLay.addWidget(self.canvas.toolbar) # Matplotlib toolbar, in case we want the user to zoom in.
        self.ui.histogramLay.addWidget(self.canvas)

    def __reconnectControls(self):
        def f():
            self.disconnectGroup("idx")
            self._connectStateUi(self.dynamic_state_ui_connections, ConceptModel.instance(), signal=None, group="idx", update_after_connect=True, idx=self.idx) # TODO: NO! Does not update on new concept
        return f


    def __conceptScannedCallback(self):
        def f(concept, out):
            QtW.QApplication.instance().scannedConcept.emit(concept[0], concept[1])
        return f

    def __updateStats(self):
        def f(idx=None, advanced_scan=None):
            if idx is None or idx == self.idx:
                stats_dict = ConceptModel.instance().pretty_print_stats(self.idx)

                for k, v in {
                    "fileSizeLbl": "file_size",
                    "processingTimeLbl": "processing_time",
                    "dirCountLbl": "dir_count",
                    "imageCountLbl": "image_count",
                    "imageCountMaskLbl": "image_count_mask",
                    "imageCountCaptionLbl": "image_count_caption",
                    "videoCountLbl": "video_count",
                    "videoCountCaptionLbl": "video_count_caption",
                    "maskCountLbl": "mask_count",
                    "maskCountUnpairedLbl": "mask_count_unpaired",
                    "captionCountLbl": "caption_count",
                    "unpairedCaptionsLbl": "unpaired_captions",
                    "maxPixelsLbl": "max_pixels",
                    "avgPixelsLbl": "avg_pixels",
                    "minPixelsLbl": "min_pixels",
                    "lengthMaxLbl": "length_max",
                    "lengthAvgLbl": "length_avg",
                    "lengthMinLbl": "length_min",
                    "fpsMaxLbl": "fps_max",
                    "fpsAvgLbl": "fps_avg",
                    "fpsMinLbl": "fps_min",
                    "captionMaxLbl": "caption_max",
                    "captionAvgLbl": "caption_avg",
                    "captionMinLbl": "caption_min",
                    "smallBucketLbl": "small_bucket",
                }.items():
                    self.ui.findChild(QtW.QLabel, k).setText(str(stats_dict[v]))

                self.__updateHistogram(stats_dict)
        return f

    def __updateHistogram(self, stats_dict):
        self.bucket_ax.cla()
        self.canvas.figure.tight_layout()
        self.canvas.figure.subplots_adjust(bottom=0.15)
        self.bucket_ax.spines['top'].set_visible(False)
        self.bucket_ax.tick_params(axis='x', which="both")
        self.bucket_ax.tick_params(axis='y', which="both")
        aspects = [str(x) for x in list(stats_dict["aspect_buckets"].keys())]
        aspect_ratios = [ConceptModel.instance().decimal_to_aspect_ratio(x) for x in
                         list(stats_dict["aspect_buckets"].keys())]
        counts = list(stats_dict["aspect_buckets"].values())
        b = self.bucket_ax.bar(aspect_ratios, counts)
        self.bucket_ax.bar_label(b)
        sec = self.bucket_ax.secondary_xaxis(location=-0.1)
        sec.spines["bottom"].set_linewidth(0)
        sec.set_xticks([0, (len(aspects) - 1) / 2, len(aspects) - 1], labels=["Wide", "Square", "Tall"])
        sec.tick_params('x', length=0)
        self.canvas.draw_idle()

    def __enableTimer(self):
        def f(idx):
            self.timer.setInterval(500)
            self.timer.start()
        return f

    def __scanConcept(self):
        def f(elem):
            # elem[0] = concept idx, elem[1] basic/advanced scanning
            return ConceptModel.instance().get_concept_stats(elem[0], elem[1])

        return f

    def __addConcept(self, advanced_scanning, first=False):
        def f():
            self.worker.enqueue((self.idx, advanced_scanning), first=first)
        return f

    def __abortScan(self):
        def f():
            ConceptModel.instance().cancel_current_concept_stats()
            self.worker.flush()
        return f

    def __updateTitle(self):
        def f():
            if not self.ui.isVisible():
                self.timer.stop() # Since QDialog has no signal for a closed window, the timer is disabled here instead.

            base_title = QCA.translate("edit_concept_status", "Edit Concept")
            processing_string = QCA.translate("edit_concept_status", "(Scanning {}...)")

            current_input = self.worker.getCurrentInput()

            if current_input is not None:
                path = ConceptModel.instance().getState("{}.path".format(current_input[0]))
                self.ui.setWindowTitle(base_title + " " + processing_string.format(path))
            else:
                self.ui.setWindowTitle(base_title)

        return f

    def __enablePromptSource(self):
        def f(_):
            if self.ui.promptSourceCmb.currentData() != "concept": # TODO: Replace with "PromptSource.CONCEPT" when ConceptConfig will accept enum instead of string.
                self.ui.promptSourceLed.setEnabled(False)
                self.ui.promptSourceBtn.setEnabled(False)
            else:
                self.ui.promptSourceLed.setEnabled(True)
                self.ui.promptSourceBtn.setEnabled(True)
        return f

    def __prevImage(self):
        def f():
            self.file_index = max(0, self.file_index - 1)
            self.__updateImage()()
        return f

    def __nextImage(self):
        def f():
            image_count = ConceptModel.instance().getState("{}.concept_stats.image_count".format(self.idx))
            self.file_index = min(image_count - 1, self.file_index + 1) if image_count is not None else self.file_index + 1
            self.__updateImage()()
        return f

    def __updateImage(self):
        def f():
            img, filename, caption = ConceptModel.instance().getImage(self.idx, self.file_index, show_augmentations=self.ui.showAugmentationsCbx.isChecked())
            self.ui.previewLbl.setPixmap(QtGui.QPixmap.fromImage(ImageQt(img)))
            self.ui.filenameLbl.setText(filename)
            self.ui.promptTed.setPlainText(caption)
        return f

    def __updateConcept(self):
        def f(idx):
            self.idx = idx
            self.file_index = 0

            self.ui.nameLed.setText(ConceptModel.instance().get_concept_name(self.idx)) # Name has a different logic than other controls and cannot exploit the connection dictionary.
        return f

    def __saveConcept(self):
        def f():
            ConceptModel.instance().setState("{}.name".format(self.idx), self.ui.nameLed.text())

            # No need to store statistics, as they are handled directly by the model.
            QtW.QApplication.instance().conceptsChanged.emit()
            self.ui.hide()
        return f

    def _connectUIBehavior(self):
        self._connectFileDialog(self.ui.pathBtn, self.ui.pathLed, is_dir=True, title=QCA.translate("dialog_window", "Open Dataset directory"))
        self._connectFileDialog(self.ui.promptSourceBtn, self.ui.promptSourceLed, is_dir=False,
                               title=QCA.translate("dialog_window", "Open Prompt Source"),
                               filters=QCA.translate("filetype_filters",
                                                     "Text (*.txt)"))

        self.connect(QtW.QApplication.instance().openConcept, self.__updateConcept())
        self.connect(QtW.QApplication.instance().openConcept, self.__updateStats())
        self.connect(self.ui.okBtn.clicked, self.__saveConcept())

        self.connect(QtW.QApplication.instance().scannedConcept, self.__updateStats())

        # TODO: connect conceptsChanged with a global basic scanning


    def _connectInputValidation(self):
        self.connect(self.ui.promptSourceCmb.activated, self.__enablePromptSource())
        self.connect(self.ui.refreshBasicBtn.clicked, self.__addConcept(advanced_scanning=False, first=True))
        self.connect(self.ui.refreshAdvancedBtn.clicked, self.__addConcept(advanced_scanning=True, first=True))
        self.connect(self.ui.abortScanBtn.clicked, self.__abortScan())
        self.connect(self.ui.updatePreviewBtn.clicked, self.__updateImage())
        self.connect(self.ui.prevBtn.clicked, self.__prevImage())
        self.connect(self.ui.nextBtn.clicked, self.__nextImage())


    def _loadPresets(self):
        for e in PromptSource.enabled_values():
            self.ui.promptSourceCmb.addItem(e.pretty_print(), userData=str(e)) # ConceptConfig serializes string, not enum

        for e in DropoutMode.enabled_values():
            self.ui.dropoutModeCmb.addItem(e.pretty_print(), userData=str(e)) # ConceptConfig serializes string, not enum

        for e in SpecialDropoutTags.enabled_values():
            self.ui.specialDropoutTagsCmb.addItem(e.pretty_print(), userData=str(e)) # ConceptConfig serializes string, not enum

        for e in BalancingStrategy.enabled_values():
            self.ui.balancingCmb.addItem(e.pretty_print(), userData=e)

        # TODO: this always allows Prior Validation concepts, even when LORA is not selected. (The behavior is the same as original OneTrainer, delegating checks to non-ui methods).
        for e in ConceptType.enabled_values(context="prior_pred_enabled"):
            self.ui.conceptTypeCmb.addItem(e.pretty_print(), userData=e)