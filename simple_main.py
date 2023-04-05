import random
import threading

from flask import Flask, render_template, request, jsonify

from content_data import Story
from content_procurement import get_parametric_prompt
from dalle.dalle import generate_image_and_return_url
from gpt.gpt import prompt_completion_chat

app = Flask(__name__)

ss = Story()
print("Made story: ", ss.tone, ss.protagonist, ss.macguffin, ss.style)
recently_updated = False


@app.route('/', methods=['GET', 'POST'])
def index():
    global ss
    print("Index being called!")
    if request.method == 'POST':
        text = request.form['text']
        bottom_text = request.form['bottom_text']
        image_url = request.form['image_url']
    else:
        text = ss.description
        bottom_text = '\n\n'.join(ss.paragraphs)
        image_url = '/static/tmp.jpeg' if ss.picture is None else ss.picture
    print("Rendering story: ", ss.tone, ss.protagonist, ss.macguffin, ss.style)
    return render_template('multi_panel.html', top_text=text, bottom_text=bottom_text, image_url=image_url, tone=ss.tone, protagonist=ss.protagonist, macguffin=ss.macguffin, style_inspo=ss.style)


def create_simple_story():
    global recently_updated, ss
    sys_desc = "You are a brilliant writer."
    prompt = get_parametric_prompt(ss.tone, ss.protagonist, ss.macguffin, ss.style)
    story_description = prompt_completion_chat(prompt, system_description=sys_desc)
    print(f"Task completed, result: {story_description}")
    ss.description = story_description
    recently_updated = True

    # Get a picture from DALLE
    ss.picture = generate_image_and_return_url(story_description)
    recently_updated = True

    # Simple story structure
    # Setting the scene
    prompt = f"Story outline: {story_description}.\n\nMaintaining the same tone, write one sentence to establish the scene for this story:"
    scene = prompt_completion_chat(prompt, system_description=sys_desc)
    print(f"Scene completed, result: {scene}")
    ss.paragraphs.append(scene)
    recently_updated = True

    # A conflict occurs
    prompt = f"Story outline: {story_description}.\n\nMaintaining the same tone, write one sentence to establish the scene for this story:\n\n{scene}\n\nNow, write one sentence to establish a conflict for this story:"
    conflict = prompt_completion_chat(prompt, system_description=sys_desc)
    print(f"Conflict completed, result: {conflict}")
    ss.paragraphs.append(conflict)
    recently_updated = True

    # We learn something about the characters
    char_det = random.choice(['fun', 'alarming', 'heartwarming', 'interesting'])
    prompt = f"Story outline: {story_description}.\n\nMaintaining the same tone, write one sentence to establish the scene for this story:\n\n{scene}\n\nNow, write one sentence to establish a conflict for this story:\n\n{conflict}\n\nNow, write one sentence in which we learn something {char_det} about one of the characters:"
    character_info = prompt_completion_chat(prompt, system_description=sys_desc)
    print(f"Character Info completed, result: {character_info}")
    ss.paragraphs.append(character_info)
    recently_updated = True

    # The conflict is resolved
    prompt = f"Story outline: {story_description}.\n\nMaintaining the same tone, write one sentence to establish the scene for this story:\n\n{scene}\n\nNow, write one sentence to establish a conflict for this story:\n\n{conflict}\n\nNow, write one sentence in which we learn something {char_det} about one of the characters:\n\n{character_info}\n\nNow, write one sentence in which the conflict is resolved:"
    conflict_resolved = prompt_completion_chat(prompt, system_description=sys_desc)
    print(f"Conflict Resolved completed, result: {conflict_resolved}")
    ss.paragraphs.append(conflict_resolved)
    recently_updated = True


@app.route('/should_refresh')
def should_refresh():
    global recently_updated
    ru = recently_updated
    recently_updated = False
    return str(ru)


@app.route('/new_story', methods=['POST'])
def new_story():
    global ss, recently_updated
    print("Making a new story")
    recently_updated = True

    tone = request.form['tone']
    protagonist = request.form['protagonist']
    macguffin = request.form['macguffin']
    style_inspo = request.form['style_inspo']

    print("BUTTON PRESSED!", tone, protagonist, macguffin, style_inspo)

    ss = Story()
    ss.tone = tone
    ss.protagonist = protagonist
    ss.macguffin = macguffin
    ss.style = style_inspo

    refresh_thread = threading.Thread(target=create_simple_story)
    refresh_thread.start()

    return jsonify({}), 204


if __name__ == "__main__":
    print("Thread time")
    refresh_thread = threading.Thread(target=create_simple_story)
    refresh_thread.start()
    app.run(debug=True)
