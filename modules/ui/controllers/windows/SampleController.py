from modules.ui.controllers.BaseController import BaseController
from modules.ui.controllers.widgets.SampleParamsController import SampleParamsController

from modules.ui.models.SamplingModel import SamplingModel

from modules.ui.utils.WorkerPool import WorkerPool

from PIL.ImageQt import ImageQt
import PySide6.QtGui as QtGui


class SampleController(BaseController):
    def __init__(self, loader, parent=None):
        super().__init__(loader, "modules/ui/views/windows/sample.ui", name=None, parent=parent)

    def _setup(self):
        self.samplingParams = SampleParamsController(self.loader, model_instance=SamplingModel.instance(), parent=self.parent)
        self.ui.paramsLay.addWidget(self.samplingParams.ui)

    def _connectUIBehavior(self):
        self.connect(self.ui.sampleBtn.clicked, self.__startSample())

        self.__enableControls(True)()

    def __sample(self):
        def f(progress_fn=None):
            SamplingModel.instance().sample(progress_fn=progress_fn)
        return f

    def __startSample(self):
        def f():
            worker, name = WorkerPool.instance().createNamed(self.__sample(), "sample_image", inject_progress_callback=True)
            if worker is not None:
                worker.connect(init_fn=self.__enableControls(False), result_fn=None,
                               finished_fn=self.__enableControls(True),
                               errored_fn=self.__enableControls(True), aborted_fn=self.__enableControls(True),
                               progress_fn=self.__updateStatus())
                WorkerPool.instance().start(name)

        return f

    def __enableControls(self, enabled):
        def f():
            self.ui.sampleBtn.setEnabled(enabled)
            if enabled:
                self.ui.progressBar.setValue(0)
        return f

    def __updateStatus(self):
        progress_fn = self._updateProgress(self.ui.progressBar)
        def f(data):
            if "status" in data:
                self.ui.statusLbl.setText(data["status"])

            if "data" in data:
                self.ui.previewLbl.setPixmap(QtGui.QPixmap.fromImage(ImageQt(data["data"])))

            progress_fn(data)
        return f