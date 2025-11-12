from PySide6.QtCore import QSemaphore, QThread, QBasicMutex
import PySide6.QtWidgets as QtW

# Generic worker thread class. It allows to process arbitrary data, with an arbitrary function.
# The implementation is a classic concurrent programming exercise, with the usual caveats (run should never be invoked directly, make sure to wait() before terminating the application, etc.)
# New data to be processed can be added at the beginning or end of the queue, up to an optional max_queue_size limit.
# For simplicity's sake, outputs are simply polled (I am assuming the caller cannot wait to acquire a semaphore, and that we do not want to implement async logic in GUI code).
# Important assumption: worker_fn must be terminating (otherwise there is no way to signal the thread to stop/abort) and it should not raise any exception.
# To be extra-safe, do not use this class to process a list of GPU-bound operations (e.g., captioning in the background), as the class is non-singleton and multiple threads may be running at the same time, possibly depleting VRAM.

# This approach is discouraged by the official QT documentation, in favor of a moveToThread() approach, where the thread lives on its own event loop and data is passed via slots and signals (implicitly enqueuing successive requests), making it slightly more efficient and significantly easier to debug.
# However, the signaling mechanism is always FIFO, therefore we would not have the possibility of inserting high-priority data to be processed first, without a convoluted priority logic.
# See here for further information: https://stackoverflow.com/questions/50622536/movetothread-vs-deriving-from-qthread-in-qt

# A third option would be launching a different QRunnable for each element of the queue, but this would not guarantee in-order processing.

# TODO: if instead of QThread, uses threading.Thread, it can use threading events, preserving the old interface of modules.util.concept_stats...


class WorkerThread(QThread):
    def __init__(self, worker_fn, on_end_fn=None, abort_fn=None, max_queue_size=None, terminate_on_empty=False, wakeup_time=500):
        super().__init__()
        self.worker_fn = worker_fn
        self.on_end_fn = on_end_fn
        self.abort_fn = abort_fn
        self.max_queue_size = max_queue_size
        self.terminate_on_empty = terminate_on_empty
        self.wakeup_time = wakeup_time

        self.queue = []
        self.current_input = None
        self.last_output = None
        self.mutex = QBasicMutex()
        self.semaphore = QSemaphore()

        QtW.QApplication.instance().aboutToQuit.connect(self.onQuit()) # TODO: CHECK THAT THIS DOES NOT CREATE DEADLOCKS NOR KEEPS A ZOMBIE THREAD/PROCESS ON EXIT


    def run(self):
        self.mutex.lock()
        self.mutex.unlock()

        while not self.isInterruptionRequested():
            print("LOOPING")
            if self.semaphore.tryAcquire(1, self.wakeup_time):
                self.semaphore.acquire()
                self.mutex.lock()
                ci = self.queue.pop(0)
                self.current_input = ci
                self.mutex.unlock()

                out = self.worker_fn(self.current_input) # TODO: DEADLOCK HERE IF APPLICATION IS CLOSED DURING ADVANCED SCAN -> If we cannot solve the deadlock, maybe it is better to restore original threading implementation and use the same logic of tkinter
                if self.on_end_fn is not None:
                    self.on_end_fn(ci, out)

                self.mutex.lock()
                self.last_output = out
                self.current_input = None
                self.mutex.unlock()

                if self.terminate_on_empty and len(self.queue) == 0:
                    self.requestInterruption()
        print("LOOP TERMINATED")


    def stop(self):
        if self.abort_fn is not None:
            self.abort_fn()
        self.requestInterruption()
        print("REQUESTED INTERRUPTION")

    def flush(self):
        self.mutex.lock()
        self.queue = []
        self.mutex.unlock()

    def __len__(self):
        self.mutex.lock()
        out = len(self.queue)
        self.mutex.unlock()
        
        return out


    def enqueue(self, item, first=False):
        self.mutex.lock()
        if self.max_queue_size is not None:
            out = len(self.queue) < self.max_queue_size
        else:
            out = True
        self.mutex.unlock()

        if out:
            self.semaphore.release()
            self.mutex.lock()
            if first:
                self.queue.insert(0, item)
            else:
                self.queue.append(item)
            self.mutex.unlock()

        return out

    def getLastOutput(self):
        self.mutex.lock()
        out = self.last_output
        self.mutex.unlock()

        return out

    def getCurrentInput(self):
        self.mutex.lock()
        out = self.current_input
        self.mutex.unlock()

        return out

    def onQuit(self):
        def f():
            self.stop()
            self.wait()
        return f
