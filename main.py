from flask import Flask, jsonify, render_template
import time
from progresser import Task, ProgressMaker, make_example_data

app = Flask(__name__)



pm = ProgressMaker(make_example_data())


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/progress')
def progress():
    pm.make_progress()
    return jsonify(pm.get_progress_report())


if __name__ == '__main__':
    app.run(debug=True)
