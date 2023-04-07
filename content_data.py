# This file contains data types
import random
from dataclasses import dataclass


@dataclass
class Character:
    def __init__(self):
        self.name = "Character"
        self.description = ""
        self.initialized = False


@dataclass
class Location:
    def __init__(self):
        self.name = "Location"
        self.description = ""
        self.initialized = False


@dataclass
class Item:
    def __init__(self):
        self.name = "Item"
        self.description = ""
        self.initialized = False


@dataclass
class Event:
    def __init__(self):
        self.name = "Event"
        self.description = ""
        self.initialized = False


@dataclass
class Scene:
    def __init__(self):
        self.name = "Scene"
        self.description = ""
        self.prose = ""
        self.initialized = False
        self.characters = []
        self.locations = []
        self.items = []
        self.events = []


@dataclass
class Story:
    def __init__(self):
        self.name = "Story"
        self.description = ""
        self.initialized = False
        self.characters = []
        self.locations = []
        self.items = []
        self.events = []
        self.scenes = []
        self.paragraphs = []
        self.picture = None
        self.content_recently_updated = False  # Used by the UI to know when to update the content

        # Parameters
        self.tone = random.choice(
            ['silly', 'arrogant', 'fun', 'crazy', 'stupid', 'dumb', 'smart', 'clever', 'funny', 'fun', 'interesting',
             'boring', 'bland'])
        self.protagonist = random.choice(
            ['dog', 'bird', 'elephant', 'weasel', 'mongoose', 'cat', 'blue jay', 'stranger', 'wizard'])
        self.macguffin = random.choice(
            ['gold', 'true love', 'a new friend', 'a new enemy', 'a new home', 'a new family', 'a new job',
             'a new life', 'a new purpose', 'a new meaning', 'a new reason to live', 'the greatest treasure of all',
             'bees!', 'a magic portal'])
        self.style = random.choice(
            ['JK Rowling', 'JRR Tolkien', 'Octavia Butler', 'The King James Bible', 'Shakespeare', 'Mark Twain',
             'a technical manual', 'hacker leet speak', 'the Spanish language', 'the US Patent Office'])
