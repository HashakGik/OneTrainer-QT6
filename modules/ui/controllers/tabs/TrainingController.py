from PySide6 import QtWidgets
from PySide6.QtCore import QCoreApplication as QCA
from modules.ui.controllers.BaseController import BaseController

from modules.ui.controllers.windows.OptimizerController import OptimizerController

from modules.util.enum.ModelFlags import ModelFlags
import PySide6.QtWidgets as QtW
import PySide6.QtGui as QtGui

import random


from modules.util.enum.TimeUnit import TimeUnit
from modules.util.enum.TimestepDistribution import TimestepDistribution
from modules.util.enum.LearningRateScaler import LearningRateScaler
from modules.util.enum.LearningRateScheduler import LearningRateScheduler
from modules.util.enum.LossScaler import LossScaler
from modules.util.enum.LossWeight import LossWeight
from modules.util.enum.Optimizer import Optimizer
from modules.util.enum.EMAMode import EMAMode
from modules.util.enum.DataType import DataType
from modules.util.enum.GradientCheckpointingMethod import GradientCheckpointingMethod

from modules.ui.models.StateModel import StateModel
from modules.ui.models.TimestepGenerator import TimestepGenerator

from modules.ui.utils.FigureWidget import FigureWidget
from matplotlib import pyplot as plt


class TrainingController(BaseController):
    state_ui_connections = {
        "optimizer.optimizer": "optimizerCmb",
        "learning_rate_scheduler": "schedulerCmb",
        "learning_rate": "learningRateLed",
        "learning_rate_warmup_steps": "warmupStepsSbx",
        "learning_rate_min_factor": "minFactorSbx",
        "learning_rate_cycles": "cyclesSbx",
        "epochs": "epochsSbx",
        "batch_size": "batchSizeSbx",
        "gradient_accumulation_steps": "accumulationStepsSbx",
        "learning_rate_scaler": "scalerCmb",
        "clip_grad_norm": "clipGradNormSbx",

        "ema": "emaCmb",
        "ema_decay": "emaDecaySbx",
        "ema_update_step_interval": "emaUpdateIntervalSbx",
        "gradient_checkpointing": "gradientCheckpointingCmb",
        "enable_async_offloading": "asyncOffloadCbx",
        "enable_activation_offloading": "offloadActivationsCbx",
        "layer_offload_fraction": "layerOffloadFractionSbx",
        "train_dtype": "trainDTypeCmb",
        "fallback_train_dtype": "fallbackDTypeCmb",
        "enable_autocast_cache": "autocastCacheCbx",
        "resolution": "resolutionLed",
        "frames": "framesSbx",
        "force_circular_padding": "circularPaddingCbx",

        "masked_training": "maskedTrainingCbx",
        "unmasked_probability": "unmaskedProbabilitySbx",
        "unmasked_weight": "unmaskedWeightSbx",
        "normalize_masked_area_loss": "normalizeMaskedAreaCbx",
        "masked_prior_preservation_weight": "maskedPriorPreservationSbx",
        "custom_conditioning_image": "customConditioningImageCbx",
        "mse_strength": "mseSbx",
        "mae_strength": "maeSbx",
        "log_cosh_strength": "logcoshSbx",
        "vb_loss_strength": "vbLossSbx",
        "loss_weight_fn": "lossWeightFunctionCmb",
        "loss_weight_strength": "gammaSbx",
        "loss_scaler": "lossScalerCmb",

        "layer_filter_preset": "layerFilterCmb",
        "layer_filter": "layerFilterLed",
        "layer_filter_regex": "layerFilterRegexCbx",

        "embedding_learning_rate": "embeddingLearningRateLed",
        "preserve_embedding_norm": "embeddingNormCbx",

        "offset_noise_weight": "offsetNoiseWeightSbx",
        "generalized_offset_noise": "generalizedOffsetNoiseCbx",
        "perturbation_noise_weight": "perturbationNoiseWeightSbx",
        "timestep_distribution": "timestepDistributionCmb",
        "min_noising_strength": "minNoisingStrengthSbx",
        "max_noising_strength": "maxNoisingStrengthSbx",
        "noising_weight": "noisingWeightSbx",
        "noising_bias": "noisingBiasSbx",
        "timestep_shift": "timestepShiftSbx",
        "dynamic_timestep_shifting": "dynamicTimestepShiftingCbx",

        "text_encoder.include": "te1IncludeCbx",
        "text_encoder.train": "te1TrainCbx",
        "text_encoder.train_embedding": "te1TrainEmbCbx",
        "text_encoder.dropout_probability": "te1DropoutSbx",
        "text_encoder.stop_training_after": "te1StopTrainingSbx",
        "text_encoder.stop_training_after_unit": "te1StopTrainingCmb",
        "text_encoder.learning_rate": "te1LearningRateLed",
        "text_encoder_layer_skip": "te1ClipSkipSbx",

        "text_encoder_2.include": "te2IncludeCbx",
        "text_encoder_2.train": "te2TrainCbx",
        "text_encoder_2.train_embedding": "te2TrainEmbCbx",
        "text_encoder_2.dropout_probability": "te2DropoutSbx",
        "text_encoder_2.stop_training_after": "te2StopTrainingSbx",
        "text_encoder_2.stop_training_after_unit": "te2StopTrainingCmb",
        "text_encoder_2.learning_rate": "te2LearningRateLed",
        "text_encoder_2_layer_skip": "te2ClipSkipSbx",

        "text_encoder_3.include": "te3IncludeCbx",
        "text_encoder_3.train": "te3TrainCbx",
        "text_encoder_3.train_embedding": "te3TrainEmbCbx",
        "text_encoder_3.dropout_probability": "te3DropoutSbx",
        "text_encoder_3.stop_training_after": "te3StopTrainingSbx",
        "text_encoder_3.stop_training_after_unit": "te3StopTrainingCmb",
        "text_encoder_3.learning_rate": "te3LearningRateLed",
        "text_encoder_3_layer_skip": "te3ClipSkipSbx",

        "text_encoder_4.include": "te4IncludeCbx",
        "text_encoder_4.train": "te4TrainCbx",
        "text_encoder_4.train_embedding": "te4TrainEmbCbx",
        "text_encoder_4.dropout_probability": "te4DropoutSbx",
        "text_encoder_4.stop_training_after": "te4StopTrainingSbx",
        "text_encoder_4.stop_training_after_unit": "te4StopTrainingCmb",
        "text_encoder_4.learning_rate": "te4LearningRateLed",
        "text_encoder_4_layer_skip": "te4ClipSkipSbx",

        "unet.train": "unetTrainCbx",
        "unet.stop_training_after": "unetStopSbx",
        "unet.stop_training_after_unit": "unetStopCmb",
        "unet.learning_rate": "unetLearningRateLed",
        "rescale_noise_scheduler_to_zero_terminal_snr": "unetRescaleCbx",

        "prior.train": ["transformerTrainCbx", "priorTrainCbx"],
        "prior.stop_training_after": ["transformerStopSbx", "priorStopSbx"],
        "prior.stop_training_after_unit": ["transformerStopCmb", "priorStopCmb"],
        "prior.learning_rate": ["transformerLearningRateLed", "priorLearningRateLed"],
        "prior.attention_mask": "transformerAttnMaskCbx",
        "prior.guidance_scale": "transformerGuidanceSbx",

        "custom_learning_rate_scheduler": "schedulerClassLed",
    }

    def __init__(self, loader, parent=None):
        super().__init__(loader, "modules/ui/views/tabs/training.ui", name=QCA.translate("main_window_tabs", "Training"), parent=parent)

    def _setup(self):
        self.optimizer_window = OptimizerController(self.loader, parent=self)

        plt.set_loglevel('WARNING')  # suppress errors about data type in bar chart

        self.canvas = FigureWidget(parent=self.ui, width=4, height=4, zoom_tools=True)
        self.canvas.setFixedHeight(300)

        self.ax = self.canvas.figure.subplots()
        self.ui.previewLay.addWidget(self.canvas.toolbar)  # Matplotlib toolbar, in case we want the user to zoom in.
        self.ui.previewLay.addWidget(self.canvas)

        self.ax.tick_params(axis='x', which="both")
        self.ax.tick_params(axis='y', which="both")

    def __updatePreview(self):
        def f():
            resolution = random.randint(512, 1024)
            generator = TimestepGenerator(
                timestep_distribution=StateModel.instance().getState("timestep_distribution"),
                min_noising_strength=StateModel.instance().getState("min_noising_strength"),
                max_noising_strength=StateModel.instance().getState("max_noising_strength"),
                noising_weight=StateModel.instance().getState("noising_weight"),
                noising_bias=StateModel.instance().getState("noising_bias"),
                timestep_shift=StateModel.instance().getState("timestep_shift"),
                dynamic_timestep_shifting=StateModel.instance().getState("dynamic_timestep_shifting"),
                latent_width=resolution // 8,
                latent_height=resolution // 8,
            )

            self.ax.cla()
            self.ax.hist(generator.generate(), bins=1000, range=(0, 999))
            self.canvas.draw_idle()
        return f


    def __updateOptimizer(self):
        def f(_):
            self.optimizer_window.ui.optimizerCmb.setCurrentIndex(self.ui.optimizerCmb.currentIndex())
            QtW.QApplication.instance().optimizerChanged.emit(self.ui.optimizerCmb.currentData())
        return f

    def __updateModel(self):
        def f(model_type, training_method):
            flags = ModelFlags.getFlags(model_type, training_method)
            presets = ModelFlags.getPresets(model_type)


            self.ui.layerFilterCmb.clear()
            for k, v in presets.items():
                self.ui.layerFilterCmb.addItem(k, userData=v)
            self.ui.layerFilterCmb.addItem("custom", userData=[])

            self.ui.te1Gbx.setVisible(ModelFlags.TE1 in flags)
            self.ui.te2Gbx.setVisible(ModelFlags.TE2 in flags)
            self.ui.te3Gbx.setVisible(ModelFlags.TE3 in flags)
            self.ui.te4Gbx.setVisible(ModelFlags.TE4 in flags)

            self.ui.unetGbx.setVisible(ModelFlags.UNET in flags)
            self.ui.transformerGbx.setVisible(ModelFlags.TRANSFORMER in flags)
            self.ui.priorGbx.setVisible(ModelFlags.TRAIN_PRIOR in flags)

            self.ui.generalizedOffsetNoiseCbx.setVisible(ModelFlags.GENERALIZED_OFFSET_NOISE in flags)

            self.ui.te1IncludeCbx.setVisible(ModelFlags.TE_INCLUDE in flags)
            self.ui.te2IncludeCbx.setVisible(ModelFlags.TE_INCLUDE in flags)
            self.ui.te3IncludeCbx.setVisible(ModelFlags.TE_INCLUDE in flags)
            self.ui.te4IncludeCbx.setVisible(ModelFlags.TE_INCLUDE in flags)


            self.ui.vbLossLbl.setVisible(ModelFlags.VB_LOSS in flags)
            self.ui.vbLossSbx.setVisible(ModelFlags.VB_LOSS in flags)

            self.ui.transformerGuidanceLbl.setVisible(ModelFlags.GUIDANCE_SCALE in flags)
            self.ui.transformerGuidanceSbx.setVisible(ModelFlags.GUIDANCE_SCALE in flags)

            self.ui.dynamicTimestepShiftingCbx.setVisible(ModelFlags.DYNAMIC_TIMESTEP_SHIFTING in flags)

            self.ui.transformerAttnMaskCbx.setVisible(ModelFlags.DISABLE_FORCE_ATTN_MASK not in flags)

            self.ui.te1ClipSkipSbx.setVisible(ModelFlags.DISABLE_CLIP_SKIP not in flags)
            self.ui.te2ClipSkipSbx.setVisible(ModelFlags.DISABLE_CLIP_SKIP not in flags)
            self.ui.te3ClipSkipSbx.setVisible(ModelFlags.DISABLE_CLIP_SKIP not in flags)
            self.ui.te4ClipSkipSbx.setVisible(ModelFlags.DISABLE_CLIP_SKIP not in flags)
            self.ui.te1ClipSkipLbl.setVisible(ModelFlags.DISABLE_CLIP_SKIP not in flags)
            self.ui.te2ClipSkipLbl.setVisible(ModelFlags.DISABLE_CLIP_SKIP not in flags)
            self.ui.te3ClipSkipLbl.setVisible(ModelFlags.DISABLE_CLIP_SKIP not in flags)
            self.ui.te4ClipSkipLbl.setVisible(ModelFlags.DISABLE_CLIP_SKIP not in flags)

            self.ui.framesLbl.setVisible(ModelFlags.VIDEO_TRAINING in flags)
            self.ui.framesSbx.setVisible(ModelFlags.VIDEO_TRAINING in flags)

            self.ui.te4ClipSkipLbl.setVisible(ModelFlags.DISABLE_TE4_LAYER_SKIP not in flags)
            self.ui.te4ClipSkipSbx.setVisible(ModelFlags.DISABLE_TE4_LAYER_SKIP not in flags)

        return f

    def _connectInputValidation(self):
        self.ui.resolutionLed.setValidator(QtGui.QRegularExpressionValidator("\d+(x\d+(,\d+x\d+)*)?", self.ui))
        self.connect(self.ui.minNoisingStrengthSbx.valueChanged, self.__validateNoisingStrength("min"))
        self.connect(self.ui.maxNoisingStrengthSbx.valueChanged, self.__validateNoisingStrength("max"))

    def __validateNoisingStrength(self, direction):
        def f(value):
            min = self.ui.minNoisingStrengthSbx.value()
            max = self.ui.maxNoisingStrengthSbx.value()

            if direction == "min" and min > max:
                self.ui.minNoisingStrengthSbx.setValue(max)

            if direction == "max" and max < min:
                self.ui.maxNoisingStrengthSbx.setValue(min)

        return f

    def _connectUIBehavior(self):
        self.connect(self.ui.layerFilterCmb.activated, lambda _: self.__connectLayerFilter())

        self.connect(QtW.QApplication.instance().stateChanged, self.__updateSchedulerParams(), update_after_connect=True)
        self.connect(self.ui.tableWidget.currentCellChanged, self.__changeCell())
        self.connect(self.ui.updatePreviewBtn.clicked, self.__updatePreview())

        self.connect(QtW.QApplication.instance().modelChanged, self.__updateModel(), update_after_connect=True, initial_args=[StateModel.instance().getState("model_type"),
                 StateModel.instance().getState("training_method")])


        cb = self.__enableCustomScheduler()  # This must be connected after __updateModel, otherwise it will not enable/disable custom parameters correctly
        self.connect(self.ui.schedulerCmb.activated, cb)
        self.connect(QtW.QApplication.instance().stateChanged, cb, update_after_connect=True)

        self.connect(self.ui.optimizerBtn.clicked, lambda: self.openWindow(self.optimizer_window, fixed_size=True))
        self.connect(self.ui.optimizerCmb.activated, self.__updateOptimizer())

        # At the beginning invalidate the gui.
        self.optimizer_window.ui.optimizerCmb.setCurrentIndex(self.ui.optimizerCmb.currentIndex())

        # TODO: MASKED TRAINING ENABLE


    def __changeCell(self):
        def f(currentRow, currentColumn, previousRow, previousColumn):
            total_rows = self.ui.tableWidget.rowCount()

            key = self.ui.tableWidget.item(previousRow, 0)
            value = self.ui.tableWidget.item(previousRow, 1)

            if key is not None and value is not None and key.text() != "" and value.text() != "":
                StateModel.instance().setSchedulerParams(previousRow, key.text(), value.text())

                if previousRow == total_rows - 1 and previousColumn == 1:
                    self.ui.tableWidget.insertRow(total_rows)
                    self.ui.tableWidget.editItem(self.ui.tableWidget.item(total_rows, 0))
                    self.ui.tableWidget.setCurrentCell(total_rows, 0) # TODO: it inserts correctly a new cell, but tab selection returns to the first cell

        return f

    def __updateSchedulerParams(self):
        def f():
            param_dict = StateModel.instance().getState("scheduler_params")

            self.ui.tableWidget.clearContents()
            for idx, param in enumerate(param_dict):
                self.ui.tableWidget.insertRow(idx)
                self.ui.tableWidget.setItem(idx, 0, QtW.QTableWidgetItem(param["key"]))
                self.ui.tableWidget.setItem(idx, 1, QtW.QTableWidgetItem(param["value"]))
        return f

    def __enableCustomScheduler(self):
        def f():
            self.ui.tableWidget.setEnabled(self.ui.schedulerCmb.currentData() == LearningRateScheduler.CUSTOM)
            self.ui.schedulerClassLed.setEnabled(self.ui.schedulerCmb.currentData() == LearningRateScheduler.CUSTOM)
            self.ui.schedulerLbl.setEnabled(self.ui.schedulerCmb.currentData() == LearningRateScheduler.CUSTOM)
        return f


    def __connectLayerFilter(self):
        self.ui.layerFilterRegexCbx.setEnabled(self.ui.layerFilterCmb.currentText() == "custom")
        self.ui.layerFilterLed.setText(",".join(self.ui.layerFilterCmb.currentData()))

    def _loadPresets(self):
        for ui_name in ["unetStopCmb", "te1StopTrainingCmb", "te2StopTrainingCmb", "te3StopTrainingCmb", "te4StopTrainingCmb",
                        "priorStopCmb", "transformerStopCmb"]:
            ui_elem = self.ui.findChild(QtWidgets.QComboBox, ui_name)
            for e in TimeUnit.enabled_values():
                ui_elem.addItem(e.pretty_print(), userData=e)

        for e in TimestepDistribution.enabled_values():
            self.ui.timestepDistributionCmb.addItem(e.pretty_print(), userData=e)

        for e in LossScaler.enabled_values():
            self.ui.lossScalerCmb.addItem(e.pretty_print(), userData=e)

        for e in LossWeight.enabled_values():
            self.ui.lossWeightFunctionCmb.addItem(e.pretty_print(), userData=e)

        for e in GradientCheckpointingMethod.enabled_values():
            self.ui.gradientCheckpointingCmb.addItem(e.pretty_print(), userData=e)

        for e in EMAMode.enabled_values():
            self.ui.emaCmb.addItem(e.pretty_print(), userData=e)

        for e in LearningRateScaler.enabled_values():
            self.ui.scalerCmb.addItem(e.pretty_print(), userData=e)

        for e in Optimizer.enabled_values():
            self.ui.optimizerCmb.addItem(e.pretty_print(), userData=e)
            self.optimizer_window.ui.optimizerCmb.addItem(e.pretty_print(), userData=e)

        for e in LearningRateScheduler.enabled_values():
            self.ui.schedulerCmb.addItem(e.pretty_print(), userData=e)

        for e in DataType.enabled_values(context="training_dtype"):
            self.ui.trainDTypeCmb.addItem(e.pretty_print(), userData=e)

        for e in DataType.enabled_values(context="training_fallback"):
            self.ui.fallbackDTypeCmb.addItem(e.pretty_print(), userData=e)

