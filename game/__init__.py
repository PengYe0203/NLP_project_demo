"""
AI Text Adventure Game Package
"""

from .story_generator import (
    StoryGenerator,
    OpenAIStoryGenerator,
    ClaudeStoryGenerator,
    LocalStoryGenerator,
    create_generator
)

from .game_engine import (
    GameState,
    ContextManager,
    TextAdventureGame
)

__version__ = "0.1.0"
__all__ = [
    "StoryGenerator",
    "OpenAIStoryGenerator",
    "ClaudeStoryGenerator",
    "LocalStoryGenerator",
    "create_generator",
    "GameState",
    "ContextManager",
    "TextAdventureGame"
]
