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

class ProgressMaker:
    def __init__(self, tasks: list[Task] = None):
        self.tasks = tasks or []
        self.completed_tasks = []
        self.incomplete_tasks = []
        self.in_progress_tasks = []
        self.done_with_error = []
        self.all_results = []
        self.update_task_lists()

    def update_task_lists(self):
        self.completed_tasks = [t for t in self.tasks if t.done]
        self.incomplete_tasks = [t for t in self.tasks if not t.done]
        self.in_progress_tasks = [t for t in self.tasks if t.working]
        self.done_with_error = [t for t in self.tasks if t.error]
        self.all_results = [t.result for t in self.tasks if t.done]

    def make_progress(self):
        # Find tasks that are ready to start and start them, then update task lists
        for task in self.tasks:
            if task.ready_to_start:
                task.run()
        self.update_task_lists()

    def get_progress_report(self):
        # Return a dict with the number of tasks in each state
        deets = {
            "num_completed": len(self.completed_tasks),
            "num_incomplete": len(self.incomplete_tasks),
            "num_in_progress": len(self.in_progress_tasks),
            "num_done_with_error": len(self.done_with_error),
            # "completed": self.completed_tasks,
            # "incomplete": self.incomplete_tasks,
            # "in_progress": self.in_progress_tasks,
            # "done_with_error": self.done_with_error,
            "tasks": [f"{t.name} - {t.class_type} - DONE: {t.done} ERROR:{t.error} READY TO START: {t.ready_to_start}\n" for t in self.tasks],
            "all_done": len(self.incomplete_tasks) == 0,
            "all_results": "\n".join([str(r) for r in self.all_results]),
        }
        for t in self.tasks:
            deets[t.name] = {
                "name": t.name,
                "class_type": t.class_type,
                "status": t.get_status(),
                # "done": t.done,
                # "error": t.error,
                # "error_message": t.error_message,
                # "error_traceback": t.error_traceback,
                # "start_time": t.start_time,
                # "end_time": t.end_time,
                "duration": t.duration,
                "result": t.result,
            }.__str__()
        return deets

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