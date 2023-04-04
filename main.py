from flask import Flask, jsonify
import time

app = Flask(__name__)


class ProgressMaker:
    def __init__(self, functions):
        self.functions = functions
        self.progress = {}

    def make_progress(self):
        for func in self.functions:
            if func.__name__ not in self.progress:
                self.progress[func.__name__] = "In Progress"
            else:
                if self.progress[func.__name__] != "Completed":
                    self.progress[func.__name__] += "."
            func(self)
            self.progress[func.__name__] = "Completed"

    def function_1(self):
        time.sleep(5)

    def function_2(self):
        time.sleep(2)

    def function_3(self):
        time.sleep(1)


pm = ProgressMaker([ProgressMaker.function_1, ProgressMaker.function_2, ProgressMaker.function_3])


@app.route('/')
def index():
    pm.make_progress()
    return jsonify(pm.progress)


if __name__ == '__main__':
    app.run(debug=True)
