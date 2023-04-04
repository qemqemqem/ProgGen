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
        self.working = False
        self.done = False
        self.error = False
        self.error_message = ""
        self.error_traceback = ""
        self.start_time = None
        self.end_time = None
        self.duration = None
        self.result = None

class ProgressMaker:
    def __init__(self, tasks: list[Task] = None):
        self.tasks = tasks or []
        self.current_task_index = -1
        self.current_task = None
        self.completed_tasks = []
        self.incomplete_tasks = []

    def get_current_task(self):
        if self.current_task_index < 0:
            return None
        elif self.current_task_index >= len(self.tasks):
            return None
        else:
            return self.tasks[self.current_task_index]

    def _run_current_task(self):
        try:
            self.current_task.result = self.current_task.function()
        except Exception as e:
            self.current_task.error = True
            self.current_task.error_message = str(e)
            self.current_task.error_traceback = traceback.format_exc()
        finally:
            self.current_task.working = False
            self.current_task.done = True
            self.current_task.end_time = time.time()
            self.current_task.duration = self.current_task.end_time - self.current_task.start_time
            self.completed_tasks.append(self.current_task)
            self.current_task = None

    def make_progress(self):
        # If there is a current task in progress, return, otherwise start the next task in a background thread
        if self.current_task is not None:
            return

        self.current_task_index += 1
        self.current_task = self.get_current_task()
        self.current_task.working = True
        self.current_task.start_time = time.time()
        self.incomplete_tasks = self.tasks[self.current_task_index:]
        threading.Thread(target=self._run_current_task).start()