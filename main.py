from flask import Flask, jsonify, render_template
import time
from task_manager import Task, TaskManager, make_example_data
from content_procurement import make_example_data_gpt

app = Flask(__name__)

pm = TaskManager(make_example_data_gpt())


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/progress')
def progress():
    pm.make_progress()
    return jsonify(pm.get_progress_report())


if __name__ == '__main__':
    app.run(debug=True)
