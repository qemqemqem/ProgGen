from flask import Flask, jsonify, render_template

from content_procurement import make_example_data_gpt
from task_manager import TaskManager

app = Flask(__name__)

task_manager = TaskManager(make_example_data_gpt())


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/progress')
def progress():
    task_manager.make_progress()
    return jsonify(task_manager.get_progress_report())


if __name__ == '__main__':
    app.run(debug=True)
