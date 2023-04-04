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

class ProgressMaker:
    def __init__(self, tasks: list[Task] = None):
        self.tasks = tasks or []
        self.completed_tasks = []
        self.incomplete_tasks = []
        self.in_progress_tasks = []
        self.done_with_error = []
        self.update_task_lists()

    def update_task_lists(self):
        self.completed_tasks = [t for t in self.tasks if t.done]
        self.incomplete_tasks = [t for t in self.tasks if not t.done]
        self.in_progress_tasks = [t for t in self.tasks if t.working]
        self.done_with_error = [t for t in self.tasks if t.error]

    def make_progress(self):
        # Find tasks that are ready to start and start them, then update task lists
        for task in self.tasks:
            if task.ready_to_start:
                task.run()
        self.update_task_lists()

def make_example_data(num_fns = 10):
    def make_fn(i):
        def fn():
            time.sleep(i * 2)
            print(f"Task {i} completed")
            return i
        return fn
    return [Task(f"Task {i}", "Waiting", make_fn(i)) for i in range(num_fns)]

if __name__ == "__main__":
    pm = ProgressMaker(make_example_data())
    while len(pm.incomplete_tasks) > 0:
        pm.make_progress()
        time.sleep(1)
        print(f"Num Completed: {len(pm.completed_tasks)}, Num Incomplete: {len(pm.incomplete_tasks)}")
    print("Done!")