from task import Task
from content_data import *
from gpt.gpt import prompt_completion_chat


class StoryFiller:
    def __init__(self):
        self.story = Story()

    def get_next_task(self):
        def make_fn():
            def fn():
                prompt = "Tell a one sentence story about outer space"
                ans = prompt_completion_chat(prompt, system_description="You are a brilliant writer.")
                print(f"Task completed, result: {ans}")
                return ans
            return fn
        return None#Task("Fill Story", "StoryFiller", make_fn())