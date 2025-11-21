from PySide6.QtCore import QCoreApplication as QCA
from modules.ui.controllers.BaseController import BaseController

from modules.ui.controllers.widgets.SampleController import SampleController
from modules.ui.controllers.windows.NewSampleController import NewSampleController

from modules.util.enum.TimeUnit import TimeUnit
from modules.util.enum.ImageFormat import ImageFormat
from modules.ui.models.StateModel import StateModel

from modules.ui.models.SampleModel import SampleModel

import PySide6.QtWidgets as QtW

class SamplingController(BaseController):
    state_ui_connections = {
        "sample_after": "sampleAfterSbx",
        "sample_after_unit": "sampleAfterCmb",
        "sample_skip_first": "skipSbx",
        "sample_image_format": "formatCmb",
        "non_ema_sampling": "nonEmaCbx",
        "samples_to_tensorboard": "tensorboardCbx",
    }

    def __init__(self, loader, parent=None):
        super().__init__(loader, "modules/ui/views/tabs/sampling.ui", name=QCA.translate("main_window_tabs", "Sampling"), parent=parent)

    def _setup(self):
        self.children = []
        self.sample_window = NewSampleController(self.loader, parent=self)

    def _connectUIBehavior(self):
        self.connect(self.ui.addSampleBtn.clicked, self.__appendSample())
        self.connect(self.ui.disableBtn.clicked, self.__disableSamples())

        # TODO: sampleNowBtn, manualSampleBtn
        # TODO: configCmb read/write/ on stateChanged reload

        cb = self.__updateSamples() # Requires self.sample_window
        self.connect(QtW.QApplication.instance().samplesChanged, cb)
        self.connect(QtW.QApplication.instance().stateChanged, cb, update_after_connect=True)

        self.connect(self.ui.configCmb.textActivated, self.__loadConfig(), update_after_connect=True, initial_args=[self.ui.configCmb.currentText()])
        self.connect(QtW.QApplication.instance().stateChanged, self.__updateConfigs(), update_after_connect=True)

        cb4 = self.__saveConfig()
        self.connect(QtW.QApplication.instance().aboutToQuit, cb4)
        self.connect(QtW.QApplication.instance().samplesChanged, cb4)


    def __loadConfig(self):
        def f(filename):
            SampleModel.instance().load_config(filename)
            QtW.QApplication.instance().samplesChanged.emit()
        return f

    def __saveConfig(self):
        def f():
            SampleModel.instance().save_config()
        return f

    def __updateConfigs(self):
        def f():
            configs = SampleModel.instance().load_available_config_names("training_samples", include_default=False)
            if len(configs) == 0:
                configs.append(("samples", "training_samples/samples.json"))

            self.ui.configCmb.clear()
            for k, v in configs:
                self.ui.configCmb.addItem(k, userData=v)

            self.ui.configCmb.setCurrentIndex(self.ui.configCmb.findData(StateModel.instance().getState("sample_definition_file_name")))
        return f

    def __updateSamples(self):
        def f():
            for c in self.children:
                c.disconnectAll()

            self.ui.listWidget.clear()  # TODO: CHECK: IS IT CLEARING CORRECTLY?
            self.children = []

            for idx, _ in enumerate(SampleModel.instance().getState("")):
               wdg = SampleController(self.loader, self.sample_window, idx, parent=self)
               self.children.append(wdg)
               self._appendWidget(self.ui.listWidget, wdg, self_delete_fn=self.__deleteSample(idx), self_clone_fn=self.__cloneSample(idx))



        return f

    def __appendSample(self):
        def f():
            SampleModel.instance().create_new_sample()
            QtW.QApplication.instance().samplesChanged.emit()
        return f

    def __disableSamples(self):
        def f():
            SampleModel.instance().disable_samples()
            QtW.QApplication.instance().samplesChanged.emit()
        return f

    def __cloneSample(self, idx):
        def f():
            SampleModel.instance().clone_sample(idx)
            QtW.QApplication.instance().samplesChanged.emit()

        return f

    def __deleteSample(self, idx):
        def f():
            SampleModel.instance().delete_sample(idx)
            QtW.QApplication.instance().samplesChanged.emit()

        return f

    def _loadPresets(self):
        for e in TimeUnit.enabled_values():
            self.ui.sampleAfterCmb.addItem(e.pretty_print(), userData=e)
        for e in ImageFormat.enabled_values():
            self.ui.formatCmb.addItem(e.pretty_print(), userData=e)