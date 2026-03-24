"""
AI Story Generator for Text Adventure Game
Support for multiple AI backends (OpenAI, Claude, Local Models, etc.)
"""

import os
from typing import Optional, Dict, List
from .localization import LocalizationManager as L


class StoryGenerator:
    """Base class for story generation"""
    
    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.model_name = model_name
        self.system_prompt = self._create_system_prompt()
    
    def _create_system_prompt(self) -> str:
        """Create system prompt for story generation"""
        return L.get("system_prompt_story")
    
    def build_prompt(self, story_context: str, player_action: Optional[str] = None, 
                    game_state: Optional[Dict] = None) -> str:
        """Build the prompt for API call"""
        
        prompt = f"""【游戏状态】
位置：{game_state.get('location', '未知') if game_state else '未知'}
物品：{', '.join(game_state.get('inventory', [])) if game_state else '无'}
NPC：{', '.join(game_state.get('npcs', [])) if game_state else '无'}

【故事记录】
{story_context}

【玩家操作】
{player_action if player_action else '(玩家选择继续观看故事)'}

【要求】
根据上述信息，生成下一段故事。不要解释，直接开始叙述。"""
        
        return prompt
    
    def generate(self, story_context: str, player_action: Optional[str] = None,
                game_state: Optional[Dict] = None) -> str:
        """
        Generate next story segment
        
        Args:
            story_context: Previous story content
            player_action: Player's action (can be None for auto-continue)
            game_state: Current game state dict
        
        Returns:
            Generated story text
        """
        raise NotImplementedError("Subclass must implement generate()")


class OpenAIStoryGenerator(StoryGenerator):
    """OpenAI-based story generator"""
    
    def __init__(self, model_name: str = "gpt-4o-mini", api_key: Optional[str] = None):
        super().__init__(model_name)
        try:
            import openai
            self.openai = openai
            self.client = openai.OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        except ImportError:
            raise ImportError("Please install openai: pip install openai")
    
    def generate(self, story_context: str, player_action: Optional[str] = None,
                game_state: Optional[Dict] = None) -> str:
        """Generate story using OpenAI API"""
        
        prompt = self.build_prompt(story_context, player_action, game_state)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                top_p=0.9,
                max_tokens=300
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {e}")


class ClaudeStoryGenerator(StoryGenerator):
    """Claude-based story generator"""
    
    def __init__(self, model_name: str = "claude-3-5-sonnet-20241022", api_key: Optional[str] = None):
        super().__init__(model_name)
        try:
            import anthropic
            self.anthropic = anthropic
            self.client = anthropic.Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
        except ImportError:
            raise ImportError("Please install anthropic: pip install anthropic")
    
    def generate(self, story_context: str, player_action: Optional[str] = None,
                game_state: Optional[Dict] = None) -> str:
        """Generate story using Claude API"""
        
        prompt = self.build_prompt(story_context, player_action, game_state)
        
        try:
            response = self.client.messages.create(
                model=self.model_name,
                max_tokens=300,
                system=self.system_prompt,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            raise RuntimeError(f"Claude API error: {e}")


class LocalStoryGenerator(StoryGenerator):
    """Local model-based story generator (using Ollama or similar)"""
    
    def __init__(self, model_name: str = "llama3", api_url: str = "http://localhost:11434"):
        super().__init__(model_name)
        try:
            import requests
            self.requests = requests
            self.api_url = api_url
        except ImportError:
            raise ImportError("Please install requests: pip install requests")
    
    def generate(self, story_context: str, player_action: Optional[str] = None,
                game_state: Optional[Dict] = None) -> str:
        """Generate story using local model via Ollama"""
        
        prompt = self.build_prompt(story_context, player_action, game_state)
        
        try:
            response = self.requests.post(
                f"{self.api_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "system": self.system_prompt,
                    "stream": False
                },
                timeout=60
            )
            response.raise_for_status()
            return response.json()["response"]
        except Exception as e:
            raise RuntimeError(f"Local model error: {e}")


def create_generator(backend: str = "openai", **kwargs) -> StoryGenerator:
    """Factory function to create appropriate generator
    
    Args:
        backend: "openai", "claude", or "local"
        **kwargs: Additional arguments passed to generator
    
    Returns:
        StoryGenerator instance
    """
    generators = {
        "openai": OpenAIStoryGenerator,
        "claude": ClaudeStoryGenerator,
        "local": LocalStoryGenerator,
    }
    
    if backend not in generators:
        raise ValueError(f"Unknown backend: {backend}. Choose from {list(generators.keys())}")
    
    return generators[backend](**kwargs)
