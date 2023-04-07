import random
import time

from task_manager import Task
from gpt.gpt import prompt_completion, prompt_completion_chat


def get_silly_prompt():
    return f"In one sentence, write a {random.choice(['silly', 'arrogant', 'fun', 'crazy', 'stupid', 'dumb', 'smart', 'clever', 'funny', 'fun', 'interesting', 'boring', 'bland'])} story about a {random.choice(['dog', 'bird', 'elephant', 'weasel', 'mongoose', 'cat', 'blue jay', 'stranger', 'wizard'])} who goes on an adventure and finds {random.choice(['gold', 'true love', 'a new friend', 'a new enemy', 'a new home', 'a new family', 'a new job', 'a new life', 'a new purpose', 'a new meaning', 'a new reason to live', 'the greatest treasure of all', 'bees!', 'a magic portal'])}. Only write one sentence, and write it in the style of {random.choice(['JK Rowling', 'JRR Tolkien', 'Octavia Butler', 'The King James Bible', 'Shakespeare', 'Mark Twain', 'a technical manual', 'hacker leet speak', 'the Spanish language', 'the US Patent Office'])}."


def make_example_data_gpt(num_fns = 10):
    def make_fn(i):
        def fn():
            silly_prompt = get_silly_prompt()
            ans = prompt_completion_chat(silly_prompt, system_description="You are a brilliant writer who is hoping to one day win a Pulitzer prize. You put your heart and soul into your writing, and it shows. You are a master of the English language, and you are a master of the craft of writing.")
            print(f"Task {i} completed, result: {ans}")
            return ans
        return fn
    return [Task(f"Task {i}", "GPT Silly", make_fn(i)) for i in range(num_fns)]
