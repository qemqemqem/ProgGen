import random
import threading
import time

from gpt.gpt import prompt_completion_chat
from flask import Flask, render_template, request

app = Flask(__name__)


class SimpleStory:
    def __init__(self):
        self.description = "Not yet loaded"
        self.paragraphs = []
        self.picture = None
        self.recently_updated = False


ss = SimpleStory()


@app.route('/', methods=['GET', 'POST'])
def index():
    print("Being called!")
    if request.method == 'POST':
        text = request.form['text']
        bottom_text = request.form['bottom_text']
        image_url = request.form['image_url']
    else:
        text = ss.description
        bottom_text = '\n'.join(ss.paragraphs)
        image_url = '/static/tmp.jpeg'
    return render_template('simple_index.html', text=text, bottom_text=bottom_text, image_url=image_url)


def refresh_page():
    while True:
        time.sleep(5)  # refresh every n seconds
        # with app.test_request_context():
            # Perform any server-side updates here
        i = random.randint(0, 100)
        print("Got random number {}".format(i))
        ss.description = "Random number {}".format(i)
        ss.recently_updated = True


@app.route('/should_refresh')
def should_refresh():
    ru = ss.recently_updated
    ss.recently_updated = False
    return str(ru)


if __name__ == '__main__':
    refresh_thread = threading.Thread(target=refresh_page)
    refresh_thread.start()
    app.run(debug=True)