from flask import Flask, render_template
import time

def get_functions_to_run():
    fns = []
    for i in range(10):
        # A function that weights 1 second to run
        fns.append(lambda: time.sleep(1))
    return fns

app = Flask(__name__)

class FunctionTracker:
    def __init__(self):
        self.functions = get_functions_to_run()
        self.current_function_index = -1

    def get_current_function(self):
        if self.current_function_index < 0:
            return None
        elif self.current_function_index >= len(self.functions):
            return None
        else:
            return self.functions[self.current_function_index]

    def get_completed_functions(self):
        return self.functions[:self.current_function_index]

    def get_incomplete_functions(self):
        return self.functions[self.current_function_index:]

function_tracker = FunctionTracker()

@app.route("/")
def index():
    current_function = function_tracker.get_current_function()
    completed_functions = function_tracker.get_completed_functions()
    incomplete_functions = function_tracker.get_incomplete_functions()
    return render_template("index.html", current_function=current_function, completed_functions=completed_functions, incomplete_functions=incomplete_functions, enumerate=enumerate)

if __name__ == "__main__":
    app.run()
