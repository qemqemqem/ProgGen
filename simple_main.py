import threading
import time

from flask import Flask, render_template, request, jsonify

from story_filler import StoryFiller
from task_manager import TaskManager

app = Flask(__name__)


def refresh_site_content():
    global story, task_manager, story_filler
    task_manager = TaskManager([])  # In charge of tasks
    story_filler = StoryFiller()  # In charge of content
    task_manager.get_next_task = story_filler.get_next_task
    story = story_filler.story  # Details about the story
    print("Made story: ", story.tone, story.protagonist, story.macguffin, story.style)


@app.route('/', methods=['GET', 'POST'])
def index():
    global story, task_manager
    print("Index being called!")
    if request.method == 'POST':
        text = request.form['text']
        bottom_text = request.form['bottom_text']
        image_url = request.form['image_url']
    else:
        text = story.description if story.description != "" else "Loading..."
        bottom_text = '\n\n'.join([s.text for s in story.scenes]) if len(story.scenes) > 0 else "Writing Story..."
        image_url = '/static/tmp.jpeg' if story.picture is None else story.picture
    print("Rendering story: ", story.tone, story.protagonist, story.macguffin, story.style)
    return render_template('multi_panel.html', top_text=text, bottom_text=bottom_text, image_url=image_url,
                           tone=story.tone, protagonist=story.protagonist, macguffin=story.macguffin,
                           style_inspo=story.style,
                           details_panel=str(task_manager.get_progress_report() + "\n\n" + story_filler.get_outline_text()))


@app.route('/should_refresh')
def should_refresh():
    global story
    ru = story.content_recently_updated
    story.content_recently_updated = False
    return str(ru)


@app.route('/new_story', methods=['POST'])
def new_story():
    global story, task_manager, story_filler
    print("Making a new story")
    story.content_recently_updated = True

    tone = request.form['tone']
    protagonist = request.form['protagonist']
    macguffin = request.form['macguffin']
    style_inspo = request.form['style_inspo']

    print("BUTTON PRESSED!", tone, protagonist, macguffin, style_inspo)

    refresh_site_content()
    # story_filler.story = Story()
    story = story_filler.story
    story.tone = tone
    story.protagonist = protagonist
    story.macguffin = macguffin
    story.style = style_inspo

    refresh_thread = threading.Thread(target=run_task_manager_background)
    refresh_thread.start()

    return jsonify({}), 204


def run_task_manager_background():
    global task_manager, story_filler
    task_manager.make_progress()  # Get the first task
    while not story_filler.is_story_done():
        task_manager.make_progress()
        time.sleep(0.4)
        print(
            f"Num Completed: {len(task_manager.completed_tasks)}, Num Incomplete: {len(task_manager.incomplete_tasks)}")
    print("Done!")


refresh_site_content()

if __name__ == "__main__":
    print("Thread time")
    refresh_thread = threading.Thread(target=run_task_manager_background)
    refresh_thread.start()
    app.run(debug=True)
