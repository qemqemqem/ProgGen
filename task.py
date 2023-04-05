import threading
import time
import traceback


class Task:
    def __init__(self, name, class_type: str, function):
        self.name = name
        self.class_type = class_type
        self.function = function
        self.progress = 0
        self.total = 0
        self.ready_to_start = True
        self.working = False
        self.done = False
        self.error = False
        self.error_message = ""
        self.error_traceback = ""
        self.start_time = None
        self.end_time = None
        self.duration = None
        self.result = None

    def get_status(self):
        # Return a string with the status of the task
        if self.error:
            return "Error" + (f": {self.error_message}" if self.error_message else "")
        elif self.done:
            return "Done"
        elif self.working:
            return "Working"
        elif self.ready_to_start:
            return "Ready to Start"
        else:
            return "Unknown"

    def _run(self):
        # Run function in background thread, mark done when done
        try:
            self.result = self.function()
        except Exception as e:
            self.error = True
            self.error_message = str(e)
            self.error_traceback = traceback.format_exc()
        finally:
            self.done = True
            self.working = False
            self.end_time = time.time()
            self.duration = self.end_time - self.start_time

    def run(self):
        # Start function in background thread, mark done when done
        self.working = True
        self.ready_to_start = False
        self.start_time = time.time()
        thread = threading.Thread(target=self._run)
        thread.start()
