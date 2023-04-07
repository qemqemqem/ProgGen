from content_data import *
from content_procurement import get_parametric_prompt
from dalle.dalle import generate_image_and_return_url
from gpt.gpt import prompt_completion_chat
from task import Task
from utils.parsing import parse_bullet_points


# This is v1, not yet replaced by next steps generation
class StoryFiller:
    def __init__(self):
        self.story = Story()
        self.outline: list[str] = []
        self.complete = False
        self.overall_prompt = ""

    def get_outline_text(self):
        return '\n'.join(["* " + s for s in self.outline])

    def get_next_task(self, task_manager):
        if len(task_manager.incomplete_tasks) > 0:
            # This model is sequential
            return None

        sys_desc = f"You are a brilliant writer. You are writing a {self.story.tone} story in the style of {self.story.style}"

        if self.story.description == "":
            def story_description():
                print("GETTING DESCRIPTION")
                self.overall_prompt = get_parametric_prompt(self.story.tone, self.story.protagonist, self.story.macguffin,
                                                            self.story.style)
                story_description = prompt_completion_chat(self.overall_prompt, system_description=sys_desc)
                print(f"Task completed, result: {story_description}")
                self.story.description = story_description
                self.story.content_recently_updated = True
                return story_description

            return Task("Write a story description", "StoryFiller", story_description)

        if self.outline is None or len(self.outline) == 0:
            def story_outline():
                print("GETTING OUTLINE")
                prompt = f"Story description: {self.story.description}.\n\nWrite a outline for this story. Please use bullet points and keep it short."
                story_outline = prompt_completion_chat(prompt, system_description=sys_desc)
                print(f"Task completed, result: {story_outline}")
                outline_split = parse_bullet_points(story_outline)
                print(f"Split outline: {outline_split}")
                self.outline = outline_split
                self.story.content_recently_updated = True
                return outline_split

            return Task("Write a story outline", "Big Picture", story_outline)

        if self.story.picture is None:
            def story_picture():
                self.story.picture = generate_image_and_return_url(self.story.description)
                self.story.content_recently_updated = True
                return self.story.picture

            return Task("Get a picture", "Image", story_picture)

        if len(self.outline) > 0:
            scene_summary = self.outline[0]
            self.outline = self.outline[1:]

            def add_paragraph():
                print("ADDING PARAGRAPH")
                messages = [
                    {"role": "system", "content": sys_desc},
                    {"role": "user", "content": self.overall_prompt},
                    {"role": "assistant", "content": self.story.description}
                ]
                for scene in self.story.scenes:
                    messages.append({"role": "user", "content": f"Write a short scene for a story from this outline: {scene.prompt}"})
                    messages.append({"role": "assistant", "content": scene.text})
                messages.append({"role": "user", "content": f"Write a short one sentence scene for a story from this outline: {scene_summary}"})
                paragraph = prompt_completion_chat("", system_description=sys_desc, messages=messages)
                print(f"Task completed, result: {paragraph}")
                self.story.scenes.append(StoryElement(scene_summary, paragraph))
                self.story.content_recently_updated = True
                if len(self.outline) == 0:
                    self.complete = True
                return paragraph

            return Task(f"Add a scene from this prompt\"{scene_summary}\"", "Add Scene", add_paragraph)

        # if self.story.paragraphs is None or len(self.story.paragraphs) == 0:
        #     def set_scene():
        #         # Setting the scene
        #         prompt = f"Story outline: {self.story.description}.\n\nMaintaining the same tone, write one sentence to establish the scene for this story:"
        #         scene = prompt_completion_chat(prompt, system_description=sys_desc)
        #         print(f"Scene completed, result: {scene}")
        #         self.story.paragraphs.append(scene)
        #         self.story.content_recently_updated = True
        #         return scene
        #
        #     return Task("Write a paragraph", "StoryFiller", set_scene)
        #
        # if self.story.paragraphs is None or len(self.story.paragraphs) == 1:
        #     def add_paragraph():
        #         # A conflict occurs
        #         prompt = f"Story outline: {self.story.description}.\n\nMaintaining the same tone, write one sentence to establish the scene for this story:\n\n{self.story.paragraphs[0]}\n\nNow, write one sentence to establish a conflict for this story:"
        #         conflict = prompt_completion_chat(prompt, system_description=sys_desc)
        #         print(f"Conflict completed, result: {conflict}")
        #         self.story.paragraphs.append(conflict)
        #         self.story.content_recently_updated = True
        #         return conflict
        #
        #     return Task("Write a paragraph", "StoryFiller", add_paragraph)
        #
        # if self.story.paragraphs is None or len(self.story.paragraphs) == 2:
        #     def add_paragraph():
        #         # We learn something about the characters
        #         char_det = random.choice(['fun', 'alarming', 'heartwarming', 'interesting'])
        #         prompt = f"Story outline: {self.story.description}.\n\nMaintaining the same tone, write one sentence to establish the scene for this story:\n\n{self.story.paragraphs[0]}\n\nNow, write one sentence to establish a conflict for this story:\n\n{self.story.paragraphs[1]}\n\nNow, write one sentence in which we learn something {char_det} about one of the characters:"
        #         character_info = prompt_completion_chat(prompt, system_description=sys_desc)
        #         print(f"Character Info completed, result: {character_info}")
        #         self.story.paragraphs.append(character_info)
        #         self.story.content_recently_updated = True
        #         return character_info
        #
        #     return Task("Add Character Info", "StoryFiller", add_paragraph)
        #
        # if self.story.paragraphs is None or len(self.story.paragraphs) == 3:
        #     def add_paragraph():
        #         # The conflict is resolved
        #         prompt = f"Story outline: {self.story.description}.\n\nMaintaining the same tone, write one sentence to establish the scene for this story:\n\n{self.story.paragraphs[0]}\n\nNow, write one sentence to establish a conflict for this story:\n\n{self.story.paragraphs[1]}\n\nNow, write one sentence in which we learn something about one of the characters:\n\n{self.story.paragraphs[2]}\n\nNow, write one sentence in which the conflict is resolved:"
        #         conflict_resolved = prompt_completion_chat(prompt, system_description=sys_desc)
        #         print(f"Conflict Resolved completed, result: {conflict_resolved}")
        #         self.story.paragraphs.append(conflict_resolved)
        #         self.story.content_recently_updated = True
        #         return conflict_resolved
        #
        #     return Task("Add Conflict Resolution", "StoryFiller", add_paragraph)

        # The story is complete! We can stop here.
        self.complete = True
        return None

    def is_story_done(self):
        return self.complete
