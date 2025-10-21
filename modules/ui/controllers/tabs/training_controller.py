from PySide6 import QtWidgets
from PySide6.QtCore import QCoreApplication as QCA
from modules.ui.utils.base_controller import BaseController

from modules.ui.controllers.windows.optimizer_controller import OptimizerController

from modules.ui.utils.ModelFlags import ModelFlags
import PySide6.QtWidgets as QtW

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
        "vb_loss_strength": "vbLossSbx", # TODO: show/hide Sbx/Lbl
        "loss_weight_fn": "lossWeightFunctionCmb", # TODO LIST OF VALUES
        "loss_weight_strength": "gammaSbx",
        "loss_scaler": "lossScalerCmb",

        "layer_filter_preset": "layerFilterCmb", # TODO LIST OF PRESETS
        "layer_filter": "layerFilterLed",
        "layer_filter_regex": "layerFilterRegexCbx",

        "embedding_learning_rate": "embeddingLearningRateSbx",
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

    }

    def __init__(self, loader, state=None, mutex=None, parent=None):
        super().__init__(loader, "modules/ui/views/tabs/training.ui", state=state, mutex=mutex, name=QCA.translate("main_window_tabs", "Training"), parent=parent)

        self.optimizer_window = OptimizerController(loader, state=state, mutex=mutex, parent=self)

        callback = self.__updateModel()
        QtW.QApplication.instance().modelChanged.connect(callback)


        self.__postConnectUIBehavior()
        # At the beginning invalidate the gui.
        callback(self.state.model_type, self.state.training_method)
        self.optimizer_window.ui.optimizerCmb.setCurrentIndex(self.ui.optimizerCmb.currentIndex())


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

            pass
        return f

    def connectInputValidation(self):
        pass # TODO: resolutionLed validation, learningRateLed validation, minNoisingStrengthSbx <= maxNoisingStrengthSbx

    def connectUIBehavior(self):


        self.ui.layerFilterCmb.activated.connect(lambda _: self.__connectLayerFilter())


        # TODO: schedulerCmb enable tableWidget and schedulerClassLed if "CUSTOM" is selected.
        # tableWidget should allow to insert new rows if <Enter> is pressed on a non empty last row
        pass

    # This is called manually at the end of the constructor.
    def __postConnectUIBehavior(self): # TODO: REFACTOR! this becomes setup()
        self.ui.optimizerBtn.clicked.connect(lambda: self.openWindow(self.optimizer_window, fixed_size=True))
        self.ui.optimizerCmb.activated.connect(self.__updateOptimizer())

        for e in Optimizer:
            self.optimizer_window.ui.optimizerCmb.addItem(self._prettyPrint(e.value), userData=e)


    def __connectLayerFilter(self):
        self.ui.layerFilterRegexCbx.setEnabled(self.ui.layerFilterCmb.currentText() == "custom")
        self.ui.layerFilterLed.setText(",".join(self.ui.layerFilterCmb.currentData()))

    def loadPresets(self):
        for ui_name in ["unetStopCmb", "te1StopTrainingCmb", "te2StopTrainingCmb", "te3StopTrainingCmb", "te4StopTrainingCmb",
                        "priorStopCmb", "transformerStopCmb"]:
            ui_elem = self.ui.findChild(QtWidgets.QComboBox, ui_name)
            for e in TimeUnit:
                ui_elem.addItem(self._prettyPrint(e.value), userData=e)

        for e in TimestepDistribution:
            self.ui.timestepDistributionCmb.addItem(self._prettyPrint(e.value), userData=e)

        for e in LossScaler:
            self.ui.lossScalerCmb.addItem(self._prettyPrint(e.value), userData=e)

        for e in LossWeight:
            self.ui.lossWeightFunctionCmb.addItem(self._prettyPrint(e.value), userData=e)

        for e in GradientCheckpointingMethod:
            self.ui.gradientCheckpointingCmb.addItem(self._prettyPrint(e.value), userData=e)

        for e in EMAMode:
            self.ui.emaCmb.addItem(self._prettyPrint(e.value), userData=e)

        for e in LearningRateScaler:
            self.ui.scalerCmb.addItem(self._prettyPrint(e.value), userData=e)

        for e in Optimizer:
            self.ui.optimizerCmb.addItem(self._prettyPrint(e.value), userData=e)

        for e in LearningRateScheduler:
            self.ui.schedulerCmb.addItem(self._prettyPrint(e.value), userData=e)

        for k, v in [
            ("float32", DataType.FLOAT_32),
            ("bfloat16", DataType.BFLOAT_16)
        ]:
            self.ui.fallbackDTypeCmb.addItem(k, userData=v)

        for k, v in [
            ("float32", DataType.FLOAT_32),
            ("float16", DataType.FLOAT_16),
            ("bfloat16", DataType.BFLOAT_16),
            ("tfloat32", DataType.TFLOAT_32)
        ]:
            self.ui.trainDTypeCmb.addItem(k, userData=v)