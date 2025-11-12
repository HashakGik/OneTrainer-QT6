from PySide6.QtCore import QObject, QThreadPool, QRunnable, Signal, Slot
import sys, traceback, uuid

class Worker(QRunnable, QObject):
    finished = Signal(str)
    errored = Signal(tuple)
    result = Signal(object)

    def __init__(self, fn, name, *args, **kwargs):
        QObject.__init__(self)
        QRunnable.__init__(self)
        self.fn = fn
        self.name = name
        self.args = args
        self.kwargs = kwargs

        self.connections = {"result": [], "errored": [], "finished": []}
        self.destroyed.connect(lambda _: self.disconnectAll)

    @Slot()
    def run(self):
        try:
            out = self.fn(*self.args, **self.kwargs)
        except Exception:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.errored.emit((exctype, value, traceback.format_exc()))
        else:
            self.result.emit(out)
        finally:
            self.finished.emit(self.name)

    def connect(self, result_fn=None, finished_fn=None, errored_fn=None):
        if result_fn is not None:
            self.connections["result"].append(self.result.connect(result_fn))
        if errored_fn is not None:
            self.connections["errored"].append(self.errored.connect(errored_fn))
        if finished_fn is not None:
            self.connections["finished"].append(self.finished.connect(finished_fn))

    def disconnectAll(self):
        for k, v in self.connections.items():
            for v2 in v:
                v2.disconnect()
        self.connections = {"result": [], "errored": [], "finished": []}

# Simple worker pool class. It allows to enqueue arbitrary functions executed on a QThreadPool.
# If a job is associated with a name (runNamed()), its execution is reentrant (i.e., attempting to run the same job multiple times, will execute it only once).
# Workers (returned by runNamed and runAnonymous) expose finished(), result(function output) and errored(exception, value, traceback) signals.
# IMPORTANT: the finished signal also removes the worker reference from this class, therefore unless a reference is saved somewhere else, it will be garbage collected.
# Using the worker's connect() method, it should avoid errors due to connections still active after garbage collection.
# TODO: add a termination mechanism (ideally graceful)?
class WorkerPool:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.pool = QThreadPool()
        self.named_workers = {} # This worker's list refuses to append a new worker with the same name.
        self.anonymous_workers = {} # This worker's list can grow arbitrarily.

    def __len__(self):
        return len(self.anonymous_workers) + len(self.named_workers)

    def runAnonymous(self, fn, *args, **kwargs):
        id = str(uuid.uuid4())
        worker = Worker(fn, id, *args, **kwargs)
        worker.connect(finished_fn=self.__removeFinished(is_named=False))
        self.anonymous_workers[id] = worker
        self.pool.start(worker)
        return worker

    def runNamed(self, fn, name, *args, **kwargs):
        if name not in self.named_workers:
            worker = Worker(fn, name, *args, **kwargs)
            worker.connect(finished_fn=self.__removeFinished(is_named=True))
            self.named_workers[name] = worker
            self.pool.start(worker)
            return worker
        else:
            return None

    def __removeFinished(self, is_named):
        def f(name):
            if is_named:
                self.named_workers.pop(name)
            else:
                self.anonymous_workers.pop(name)
        return f
