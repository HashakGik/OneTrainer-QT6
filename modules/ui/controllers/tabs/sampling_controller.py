from PySide6.QtCore import QCoreApplication as QCA
from modules.ui.utils.base_controller import BaseController

from modules.ui.controllers.widgets.sample_controller import SampleController
from modules.ui.controllers.windows.new_sample_controller import NewSampleController

from modules.util.enum.TimeUnit import TimeUnit
from modules.util.enum.ImageFormat import ImageFormat


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
        self.children = []
        self.sample_window = NewSampleController(loader, parent=self)

        cb = self.__updateSamples() # Requires self.sample_window
        QtW.QApplication.instance().samplesChanged.connect(cb)
        QtW.QApplication.instance().stateChanged.connect(cb)
        cb()

        cb2 = self.__loadConfig()
        self.ui.configCmb.textActivated.connect(cb2)
        cb2(self.ui.configCmb.currentText())

    def connectUIBehavior(self):
        self.ui.addSampleBtn.clicked.connect(lambda: self.__appendSample())
        self.ui.disableBtn.clicked.connect(lambda: self.__disableSamples())

        # TODO: sampleNowBtn, manualSampleBtn
        # TODO: configCmb read/write/ on stateChanged reload





        cb3 = self.__updateConfigs()
        QtW.QApplication.instance().stateChanged.connect(cb3)

        cb4 = self.__saveConfig()
        QtW.QApplication.instance().aboutToQuit.connect(cb4)
        QtW.QApplication.instance().samplesChanged.connect(cb4)
        # TODO: this callback should also be invoked when training/sampling starts

        # At the beginning invalidate the gui.

        cb3()

    def __loadConfig(self):
        def f(filename):
            SampleModel.instance().load_config(filename)
            QtW.QApplication.instance().samplesChanged.emit()
            pass
        return f

    def __saveConfig(self):
        def f():
            SampleModel.instance().save_config()
            pass
        return f

    def __updateConfigs(self):
        def f():
            configs = SampleModel.instance().load_available_config_names("training_samples", include_default=False)
            if len(configs) == 0:
                configs.append(("samples", "training_samples/samples.json"))


            self.ui.configCmb.clear()
            for k, v in configs:
                self.ui.configCmb.addItem(k, userData=v)
        return f

    def __updateSamples(self):
        def f():
            self.ui.listWidget.clear() # TODO: Problem: THIS DESTROYS C++ OBJECTS, BUT DOES NOT DISCONNECT SIGNALS
            self.children = []

            for idx, _ in enumerate(SampleModel.instance().getState("")):
               wdg = SampleController(self.loader, self.sample_window, idx, parent=self)
               self.children.append(wdg)
               self._appendWidget(self.ui.listWidget, wdg, self_delete_fn=self.__deleteSample(idx), self_clone_fn=self.__cloneSample(idx))

        return f

    def __appendSample(self):
        SampleModel.instance().create_new_sample()
        QtW.QApplication.instance().samplesChanged.emit()
        #wdg = SampleController(self.loader, self.sample_window, len(self.children), parent=self)
        #self.children.append(wdg)
        #self._appendWidget(self.ui.listWidget, wdg, self_delete_fn=True, self_clone_fn=True)
        pass

    def __disableSamples(self):
        pass
        SampleModel.instance().disable_samples()
        QtW.QApplication.instance().samplesChanged.emit()

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

    def loadPresets(self):
        for e in TimeUnit.enabled_values():
            self.ui.sampleAfterCmb.addItem(e.pretty_print(), userData=e)
        for e in ImageFormat.enabled_values():
            self.ui.formatCmb.addItem(e.pretty_print(), userData=e)