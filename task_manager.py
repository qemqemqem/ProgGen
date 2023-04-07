import time

from task import Task


class TaskManager:
    def __init__(self, tasks: list[Task] = None):
        self.tasks = tasks or []
        self.completed_tasks = []
        self.incomplete_tasks = []
        self.in_progress_tasks = []
        self.done_with_error = []
        self.all_results = []
        self.update_task_lists()
        self.get_next_task = None

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
            next_task = self.get_next_task(self)
            if next_task:
                self.tasks.append(next_task)
        # Bookkeeping
        self.update_task_lists()
        # If at this point there are no incomplete tasks, we're done

    def get_progress_report(self):
        deets = f"num completed: {len(self.completed_tasks)}\n"
        deets += f"num incomplete: {len(self.incomplete_tasks)}\n"
        deets += f"num in progress: {len(self.in_progress_tasks)}\n"
        deets += f"num done with error: {len(self.done_with_error)}\n"
        deets += f"all done: {len(self.incomplete_tasks) == 0}\n"
        deets += "\nTASKS:\n"
        for t in self.tasks:
            print("t", t)
            deets += f"{t.name}, - STATUS: {t.get_status()}\n"

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
    task_manager = TaskManager(make_example_data())
    task_manager.get_next_task = task_manager.story_filler.get_next_task
    while len(task_manager.incomplete_tasks) > 0:
        task_manager.make_progress()
        time.sleep(1)
        print(
            f"Num Completed: {len(task_manager.completed_tasks)}, Num Incomplete: {len(task_manager.incomplete_tasks)}")
    print("Done!")
