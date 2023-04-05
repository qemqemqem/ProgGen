import random
import threading
import time

from content_procurement import get_silly_prompt
from gpt.gpt import prompt_completion_chat
from flask import Flask, render_template, request
from dalle.dalle import generate_image_and_return_url

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
        bottom_text = '\n\n'.join(ss.paragraphs)
        image_url = '/static/tmp.jpeg' if ss.picture is None else ss.picture
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


def create_simple_story():
    sys_desc = "You are a brilliant writer."
    prompt = get_silly_prompt()
    story_description = prompt_completion_chat(prompt, system_description=sys_desc)
    print(f"Task completed, result: {story_description}")
    ss.description = story_description
    ss.recently_updated = True

    # Get a picture from DALLE
    ss.picture = generate_image_and_return_url(story_description)
    ss.recently_updated = True

    # Simple story structure
    # Setting the scene
    prompt = f"Story outline: {story_description}.\n\nMaintaining the same tone, write one sentence to establish the scene for this story:"
    scene = prompt_completion_chat(prompt, system_description=sys_desc)
    print(f"Scene completed, result: {scene}")
    ss.paragraphs.append(scene)
    ss.recently_updated = True

    # A conflict occurs
    prompt = f"Story outline: {story_description}.\n\nMaintaining the same tone, write one sentence to establish the scene for this story:\n\n{scene}\n\nNow, write one sentence to establish a conflict for this story:"
    conflict = prompt_completion_chat(prompt, system_description=sys_desc)
    print(f"Conflict completed, result: {conflict}")
    ss.paragraphs.append(conflict)
    ss.recently_updated = True

    # We learn something about the characters
    char_det = random.choice(['fun', 'alarming', 'heartwarming', 'interesting'])
    prompt = f"Story outline: {story_description}.\n\nMaintaining the same tone, write one sentence to establish the scene for this story:\n\n{scene}\n\nNow, write one sentence to establish a conflict for this story:\n\n{conflict}\n\nNow, write one sentence in which we learn something {char_det} about one of the characters:"
    character_info = prompt_completion_chat(prompt, system_description=sys_desc)
    print(f"Character Info completed, result: {character_info}")
    ss.paragraphs.append(character_info)
    ss.recently_updated = True

    # The conflict is resolved
    prompt = f"Story outline: {story_description}.\n\nMaintaining the same tone, write one sentence to establish the scene for this story:\n\n{scene}\n\nNow, write one sentence to establish a conflict for this story:\n\n{conflict}\n\nNow, write one sentence in which we learn something {char_det} about one of the characters:\n\n{character_info}\n\nNow, write one sentence in which the conflict is resolved:"
    conflict_resolved = prompt_completion_chat(prompt, system_description=sys_desc)
    print(f"Conflict Resolved completed, result: {conflict_resolved}")
    ss.paragraphs.append(conflict_resolved)
    ss.recently_updated = True



@app.route('/should_refresh')
def should_refresh():
    ru = ss.recently_updated
    ss.recently_updated = False
    return str(ru)


if __name__ == '__main__':
    refresh_thread = threading.Thread(target=create_simple_story)
    refresh_thread.start()
    app.run(debug=True)