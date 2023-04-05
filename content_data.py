# This file contains data types
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


