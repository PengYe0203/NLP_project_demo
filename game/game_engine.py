"""
Game Engine for Text Adventure with AI-generated content
Handles game state, context management, and game loop
"""

import json
import os
from datetime import datetime
from typing import Optional, Dict, List, Any
from pathlib import Path
from .localization import LocalizationManager as L


class GameState:
    """Manages game state including location, inventory, NPCs, and world facts"""
    
    def __init__(self):
        self.location = "故事开始"
        self.inventory = []
        self.npcs = []
        self.world_facts = []  # Important facts to remember
        self.visited_locations = [self.location]
        self.metadata = {
            "start_time": datetime.now().isoformat(),
            "turn": 0
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary"""
        return {
            "location": self.location,
            "inventory": self.inventory,
            "npcs": self.npcs,
            "world_facts": self.world_facts,
            "visited_locations": self.visited_locations,
            "metadata": self.metadata
        }
    
    def from_dict(self, data: Dict[str, Any]) -> None:
        """Load state from dictionary"""
        self.location = data.get("location", "故事开始")
        self.inventory = data.get("inventory", [])
        self.npcs = data.get("npcs", [])
        self.world_facts = data.get("world_facts", [])
        self.visited_locations = data.get("visited_locations", [self.location])
        self.metadata = data.get("metadata", {})
    
    def extract_facts(self, text: str) -> None:
        """Extract important facts from AI response
        
        Simple pattern matching - can be enhanced with NER or LLM
        """
        # Extract items with "获得" or "得到"
        if "获得" in text or "得到" in text:
            # Very basic extraction, could be improved
            pass
        
        # Extract location changes with "到达" or "来到"
        if "到达" in text or "来到" in text or "进入" in text:
            pass
        
        # Extract NPC mentions
        for word in text.split():
            if "先生" in word or "女士" in word or "大师" in word:
                potential_npc = word.split("【")[-1].split("】")[0]
                if potential_npc not in self.npcs:
                    self.npcs.append(potential_npc)
    
    def increment_turn(self) -> None:
        """Increment turn counter"""
        self.metadata["turn"] += 1


class ContextManager:
    """Manages story context to prevent context overflow"""
    
    def __init__(self, max_history_items: int = 10, summary_threshold: int = 20):
        self.history = []
        self.max_history_items = max_history_items
        self.summary_threshold = summary_threshold
    
    def add_turn(self, action: Optional[str], story: str) -> None:
        """Add a turn to history
        
        Args:
            action: Player action (None for auto-continue)
            story: Generated story segment
        """
        self.history.append({
            "action": action or "(自动继续)",
            "story": story
        })
    
    def get_recent_context(self, num_items: int = 10) -> str:
        """Get recent context as formatted string"""
        recent = self.history[-num_items:]
        context_lines = []
        
        for item in recent:
            context_lines.append(f"【你的操作】\n{item['action']}\n")
            context_lines.append(f"【故事】\n{item['story']}\n")
        
        return "\n".join(context_lines)
    
    def get_full_context(self) -> str:
        """Get full history as string"""
        return self.get_recent_context(self.max_history_items)
    
    def clear(self) -> None:
        """Clear all history"""
        self.history = []


class TextAdventureGame:
    """Main game engine for AI-powered text adventure"""
    
    def __init__(self, story_generator, save_dir: str = "./output"):
        """
        Initialize game
        
        Args:
            story_generator: Instance of StoryGenerator (OpenAI, Claude, Local, etc.)
            save_dir: Directory to save game progress
        """
        self.generator = story_generator
        self.state = GameState()
        self.context_manager = ContextManager()
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(exist_ok=True)
        self.game_log = []
    
    def initialize_story(self) -> str:
        """Generate opening story"""
        opening_prompt = L.get("system_prompt_opening")
        
        try:
            initial_story = self.generator.generate(
                story_context="",
                player_action=None,
                game_state=self.state.to_dict()
            )
            self.context_manager.add_turn(None, initial_story)
            self.game_log.append(("init", initial_story))
            return initial_story
        except Exception as e:
            return f"{L.get('generate_failed')}: {e}"
    
    def process_action(self, action: str) -> str:
        """Process player action and generate next story segment
        
        Args:
            action: Player's action description
        
        Returns:
            Generated story text
        """
        try:
            # Get context
            context = self.context_manager.get_full_context()
            
            # Generate story
            story = self.generator.generate(
                story_context=context,
                player_action=action,
                game_state=self.state.to_dict()
            )
            
            # Update game state
            self.context_manager.add_turn(action, story)
            self.state.extract_facts(story)
            self.state.increment_turn()
            self.game_log.append(("action", action, story))
            
            return story
        except Exception as e:
            error_msg = f"{L.get('error_prefix')}: {e}"
            self.game_log.append(("error", error_msg))
            return error_msg
    
    def continue_story(self) -> str:
        """Continue story without player action (auto-continue)
        
        Returns:
            Generated story text
        """
        return self.process_action(None)
    
    def get_status(self) -> Dict[str, Any]:
        """Get current game status"""
        return {
            "state": self.state.to_dict(),
            "turn": self.state.metadata["turn"],
            "history_length": len(self.context_manager.history)
        }
    
    def save_game(self, filename: Optional[str] = None) -> str:
        """Save game progress to JSON file
        
        Args:
            filename: Custom filename (default: auto-generated)
        
        Returns:
            Path to saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"savegame_{timestamp}.json"
        
        filepath = self.save_dir / filename
        save_data = {
            "state": self.state.to_dict(),
            "game_log": self.game_log,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
        
        return str(filepath)
    
    def load_game(self, filepath: str) -> bool:
        """Load game progress from JSON file
        
        Args:
            filepath: Path to save file
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                save_data = json.load(f)
            
            self.state.from_dict(save_data["state"])
            self.game_log = save_data.get("game_log", [])
            
            # Reconstruct context
            self.context_manager.clear()
            for log_entry in self.game_log:
                if log_entry[0] == "init":
                    self.context_manager.add_turn(None, log_entry[1])
                elif log_entry[0] == "action":
                    self.context_manager.add_turn(log_entry[1], log_entry[2])
            
            return True
        except Exception as e:
            print(f"{L.get('load_failed')}: {e}")
            return False
    
    def list_saves(self) -> List[str]:
        """List all saved games"""
        return [f.name for f in self.save_dir.glob("*.json")]
