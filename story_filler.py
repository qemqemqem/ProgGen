from content_data import *
from content_procurement import get_parametric_prompt
from dalle.dalle import generate_image_and_return_url
from gpt.gpt import prompt_completion_chat
from task import Task


# This is v1, not yet replaced by next steps generation
class StoryFiller:
    def __init__(self):
        self.story = Story()

    def get_next_task(self, task_manager):
        if len(task_manager.incomplete_tasks) > 0:
            # This model is sequential
            return None

        sys_desc = f"You are a brilliant writer. You are writing a {self.story.tone} story in the style of {self.story.style}"

        if self.story.description == "":
            def story_description():
                print("GETTING DESCRIPTION")
                prompt = get_parametric_prompt(self.story.tone, self.story.protagonist, self.story.macguffin,
                                               self.story.style)
                story_description = prompt_completion_chat(prompt, system_description=sys_desc)
                print(f"Task completed, result: {story_description}")
                self.story.description = story_description
                self.story.content_recently_updated = True
                return story_description

            return Task("Write a story description", "StoryFiller", story_description)

        if self.story.picture is None:
            def story_picture():
                self.story.picture = generate_image_and_return_url(self.story.description)
                self.story.content_recently_updated = True
                return self.story.picture

            return Task("Get a picture", "StoryFiller", story_picture)

        if self.story.paragraphs is None or len(self.story.paragraphs) == 0:
            def set_scene():
                # Setting the scene
                prompt = f"Story outline: {self.story.description}.\n\nMaintaining the same tone, write one sentence to establish the scene for this story:"
                scene = prompt_completion_chat(prompt, system_description=sys_desc)
                print(f"Scene completed, result: {scene}")
                self.story.paragraphs.append(scene)
                self.story.content_recently_updated = True
                return scene

            return Task("Write a paragraph", "StoryFiller", set_scene)

        if self.story.paragraphs is None or len(self.story.paragraphs) == 1:
            def add_paragraph():
                # A conflict occurs
                prompt = f"Story outline: {self.story.description}.\n\nMaintaining the same tone, write one sentence to establish the scene for this story:\n\n{self.story.paragraphs[0]}\n\nNow, write one sentence to establish a conflict for this story:"
                conflict = prompt_completion_chat(prompt, system_description=sys_desc)
                print(f"Conflict completed, result: {conflict}")
                self.story.paragraphs.append(conflict)
                self.story.content_recently_updated = True
                return conflict

            return Task("Write a paragraph", "StoryFiller", add_paragraph)

        if self.story.paragraphs is None or len(self.story.paragraphs) == 2:
            def add_paragraph():
                # We learn something about the characters
                char_det = random.choice(['fun', 'alarming', 'heartwarming', 'interesting'])
                prompt = f"Story outline: {self.story.description}.\n\nMaintaining the same tone, write one sentence to establish the scene for this story:\n\n{self.story.paragraphs[0]}\n\nNow, write one sentence to establish a conflict for this story:\n\n{self.story.paragraphs[1]}\n\nNow, write one sentence in which we learn something {char_det} about one of the characters:"
                character_info = prompt_completion_chat(prompt, system_description=sys_desc)
                print(f"Character Info completed, result: {character_info}")
                self.story.paragraphs.append(character_info)
                self.story.content_recently_updated = True
                return character_info

            return Task("Add Character Info", "StoryFiller", add_paragraph)

        if self.story.paragraphs is None or len(self.story.paragraphs) == 3:
            def add_paragraph():
                # The conflict is resolved
                prompt = f"Story outline: {self.story.description}.\n\nMaintaining the same tone, write one sentence to establish the scene for this story:\n\n{self.story.paragraphs[0]}\n\nNow, write one sentence to establish a conflict for this story:\n\n{self.story.paragraphs[1]}\n\nNow, write one sentence in which we learn something about one of the characters:\n\n{self.story.paragraphs[2]}\n\nNow, write one sentence in which the conflict is resolved:"
                conflict_resolved = prompt_completion_chat(prompt, system_description=sys_desc)
                print(f"Conflict Resolved completed, result: {conflict_resolved}")
                self.story.paragraphs.append(conflict_resolved)
                self.story.content_recently_updated = True
                return conflict_resolved

            return Task("Add Conflict Resolution", "StoryFiller", add_paragraph)

        # The story is complete! We can stop here.
        return None  # Task("Fill Story", "StoryFiller", make_fn())

    def is_story_done(self):
        return len(self.story.paragraphs) >= 4
