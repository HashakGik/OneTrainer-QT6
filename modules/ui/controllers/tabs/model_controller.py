from PySide6.QtCore import QCoreApplication as QCA
from modules.ui.controllers.base_controller import BaseController

from modules.util.enum.ConfigPart import ConfigPart
from modules.util.enum.DataType import DataType
from modules.util.enum.ModelFormat import ModelFormat

import PySide6.QtWidgets as QtW

from modules.util.enum.ModelFlags import ModelFlags

from modules.ui.models.StateModel import StateModel

class ModelController(BaseController):
    state_ui_connections = {
        "secrets.huggingface_token": "huggingfaceLed",
        "base_model_name": "baseModelLed",
        "weight_dtype": "weightDTypeCmb",
        "output_model_destination": "modelOutputLed",
        "output_dtype": "outputDTypeCmb",
        "output_model_format": "outputFormatCmb",
        "include_train_config": "configCmb",
        "unet.weight_dtype": "unetDTypeCmb",
        "prior.weight_dtype": "priorDTypeCmb",
        "text_encoder.weight_dtype": "te1DTypeCmb",
        "text_encoder_2.weight_dtype": "te2DTypeCmb",
        "text_encoder_3.weight_dtype": "te3DTypeCmb",
        "text_encoder_4.weight_dtype": "te4DTypeCmb",
        "vae.weight_dtype": "vaeDTypeCmb",
        "effnet_encoder.weight_dtype": "effnetDTypeCmb",
        "decoder.weight_dtype": "decDTypeCmb",
        "decoder_text_encoder.weight_dtype": "decTeDTypeCmb",
        "decoder_vqgan.weight_dtype": "vqganDTypeCmb",
        "prior.model_name": "priorLed",
        "text_encoder_4.model_name": "te4Led",
        "vae.model_name": "vaeLed",
        "effnet_encoder.model_name": "effnetLed",
        "decoder.model_name": "decLed",
    }

    def __init__(self, loader, parent=None):
        super().__init__(loader, "modules/ui/views/tabs/model.ui", name=QCA.translate("main_window_tabs", "Model"), parent=parent)

    def connectUIBehavior(self):
        for ui_name in ["baseModel", "prior", "te4", "vae", "effnet", "dec"]:
            btn = self.ui.findChild(QtW.QToolButton, "{}Btn".format(ui_name))
            led = self.ui.findChild(QtW.QLineEdit, "{}Led".format(ui_name))
            self.connectFileDialog(btn, led, is_dir=False, save=False,
                               title=QCA.translate("dialog_window", "Open model"),
                               filters=QCA.translate("filetype_filters",
                                                     "Safetensors (*.safetensors);;Diffusers (model_index.json);;Checkpoints (*.ckpt, *.pt, *.bin);;All Files (*.*)"))


        self.connectFileDialog(self.ui.modelOutputBtn, self.ui.modelOutputLed, is_dir=False, save=True, # TODO: the filter of this one must be based on output format!!!
                               title=QCA.translate("dialog_window", "Save output model"),
                               filters=QCA.translate("filetype_filters",
                                                     "Safetensors (*.safetensors);;Diffusers (model_index.json);;Checkpoints (*.ckpt, *.pt, *.bin);;All Files (*.*)"))  # TODO: Maybe refactor filters in ENUM?

        callback = self.__updateModel()
        QtW.QApplication.instance().modelChanged.connect(callback)

        # At the beginning invalidate the gui.
        callback(StateModel.instance().getState("model_type"), StateModel.instance().getState("training_method"))

    def __updateModel(self):
        def f(model_type, training_method):
            flags = ModelFlags.getFlags(model_type, training_method)


            self.ui.outputFormatCmb.clear()
            if ModelFlags.ALLOW_SAFETENSORS in flags:
                self.ui.outputFormatCmb.addItem("Safetensors", userData=ModelFormat.SAFETENSORS)
            if ModelFlags.ALLOW_DIFFUSERS in flags:
                self.ui.outputFormatCmb.addItem("Diffusers", userData=ModelFormat.DIFFUSERS)
            #if ModelFlags.ALLOW_LEGACY_SAFETENSORS in flags:
            #    self.ui.outputFormatCmb.addItem("Legacy Safetensors", userData=ModelFormat.LEGACY_SAFETENSORS)

            self.ui.unetDTypeLbl.setVisible(ModelFlags.UNET in flags)
            self.ui.unetDTypeCmb.setVisible(ModelFlags.UNET in flags)

            self.ui.priorDTypeLbl.setVisible(ModelFlags.PRIOR in flags)
            self.ui.priorDTypeCmb.setVisible(ModelFlags.PRIOR in flags)

            self.ui.te1DTypeLbl.setVisible(ModelFlags.TE1 in flags)
            self.ui.te1DTypeCmb.setVisible(ModelFlags.TE1 in flags)

            self.ui.te2DTypeLbl.setVisible(ModelFlags.TE2 in flags)
            self.ui.te2DTypeCmb.setVisible(ModelFlags.TE2 in flags)

            self.ui.te3DTypeLbl.setVisible(ModelFlags.TE3 in flags)
            self.ui.te3DTypeCmb.setVisible(ModelFlags.TE3 in flags)

            self.ui.te4DTypeLbl.setVisible(ModelFlags.TE4 in flags)
            self.ui.te4DTypeCmb.setVisible(ModelFlags.TE4 in flags)

            self.ui.vaeDTypeLbl.setVisible(ModelFlags.VAE in flags)
            self.ui.vaeDTypeCmb.setVisible(ModelFlags.VAE in flags)

            self.ui.effnetLbl.setVisible(ModelFlags.EFFNET in flags)
            self.ui.effnetLed.setVisible(ModelFlags.EFFNET in flags)
            self.ui.effnetBtn.setVisible(ModelFlags.EFFNET in flags)
            self.ui.effnetDTypeLbl.setVisible(ModelFlags.EFFNET in flags)
            self.ui.effnetDTypeCmb.setVisible(ModelFlags.EFFNET in flags)

            self.ui.decDTypeLbl.setVisible(ModelFlags.DEC in flags)
            self.ui.decDTypeCmb.setVisible(ModelFlags.DEC in flags)
            self.ui.vqganDTypeLbl.setVisible(ModelFlags.DEC in flags)
            self.ui.vqganDTypeCmb.setVisible(ModelFlags.DEC in flags)

            self.ui.decTeDTypeLbl.setVisible(ModelFlags.DEC_TE in flags)
            self.ui.decTeDTypeCmb.setVisible(ModelFlags.DEC_TE in flags)

            self.ui.priorLbl.setVisible(ModelFlags.OVERRIDE_PRIOR in flags)
            self.ui.priorLed.setVisible(ModelFlags.OVERRIDE_PRIOR in flags)
            self.ui.priorBtn.setVisible(ModelFlags.OVERRIDE_PRIOR in flags)

            self.ui.te4Lbl.setVisible(ModelFlags.OVERRIDE_TE4 in flags)
            self.ui.te4Led.setVisible(ModelFlags.OVERRIDE_TE4 in flags)
            self.ui.te4Btn.setVisible(ModelFlags.OVERRIDE_TE4 in flags)

            if ModelFlags.TE1 in flags and ModelFlags.TE2 not in flags:
                self.ui.te1DTypeLbl.setText(
                    QCA.translate("model_tab_label", "Override Text Encoder Data Type")
                )
            else:
                self.ui.te1DTypeLbl.setText(
                    QCA.translate("model_tab_label", "Override Text Encoder 1 Data Type")
                )

        return f

    def loadPresets(self):
        for e in ConfigPart.enabled_values():
            self.ui.configCmb.addItem(e.pretty_print(), userData=e)

        for ui_name in ["weightDTypeCmb", "unetDTypeCmb", "priorDTypeCmb", "te1DTypeCmb", "te2DTypeCmb", "te3DTypeCmb", "te4DTypeCmb",
                        "vaeDTypeCmb", "effnetDTypeCmb", "decDTypeCmb", "decTeDTypeCmb", "vqganDTypeCmb"]:
            ui_elem = self.ui.findChild(QtW.QComboBox, ui_name)
            for e in self.__createDTypes(include_none=(ui_name=="weightDTypeCmb")):
                ui_elem.addItem(e.pretty_print(), userData=e)

        for e in DataType.enabled_values(context="output_dtype"):
            self.ui.outputDTypeCmb.addItem(e.pretty_print(), userData=e)

    def __createDTypes(self, include_none=True):
        options = DataType.enabled_values(context="model_dtypes")

        if include_none:
            options.insert(0, DataType.NONE)

        return options
