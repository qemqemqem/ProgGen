import time

from story_filler import StoryFiller
from task import Task


class ProgressMaker:
    def __init__(self, tasks: list[Task] = None):
        self.tasks = tasks or []
        self.completed_tasks = []
        self.incomplete_tasks = []
        self.in_progress_tasks = []
        self.done_with_error = []
        self.all_results = []
        self.update_task_lists()
        self.get_next_task = None
        self.story_filler = StoryFiller()

    def update_task_lists(self):
        self.completed_tasks = [t for t in self.tasks if t.done]
        self.incomplete_tasks = [t for t in self.tasks if not t.done]
        self.in_progress_tasks = [t for t in self.tasks if t.working]
        self.done_with_error = [t for t in self.tasks if t.error]
        self.all_results = [t.result for t in self.tasks if t.done]

    def make_progress(self):
        # Find tasks that are ready to start and start them
        for task in self.tasks:
            if task.ready_to_start:
                task.run()
        # Add new tasks to the list, if needed
        if self.get_next_task:
            next_task = self.get_next_task()
            if next_task:
                self.tasks.append(next_task)
        # Bookkeeping
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


def make_example_data(num_fns=10):
    def make_fn(i):
        def fn():
            time.sleep(i * 2)
            print(f"Task {i} completed")
            return i

        return fn

    return [Task(f"Task {i}", "Waiting", make_fn(i)) for i in range(num_fns)]


if __name__ == "__main__":
    pm = ProgressMaker(make_example_data())
    pm.get_next_task = pm.story_filler.get_next_task
    while len(pm.incomplete_tasks) > 0:
        pm.make_progress()
        time.sleep(1)
        print(f"Num Completed: {len(pm.completed_tasks)}, Num Incomplete: {len(pm.incomplete_tasks)}")
    print("Done!")
