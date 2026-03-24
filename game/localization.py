"""
Localization module for switching between Chinese and English
Change LANGUAGE setting to switch output language globally
"""

import os

# 设置语言: "zh" 为中文, "en" 为英文
LANGUAGE = os.getenv("GAME_LANGUAGE", "zh")


class LocalizationManager:
    """Manage multi-language strings"""
    
    STRINGS = {
        "zh": {
            # System prompts
            "system_prompt_story": """你是一个文字冒险游戏的故事叙述者。

你的responsibilities：
1. 根据玩家的行动生成沉浸式的故事段落
2. 严格遵循已建立的世界观和角色设定
3. 记住之前发生过的所有事件和玩家做过的选择
4. 保持地点、NPC、物品的名称和特性一致
5. 让玩家的操作实际影响故事发展
6. 每段故事100-200字，保留悬念

故事风格：
- 使用第二人称"你"
- 描述性但不过分冗长
- 在故事结尾给出可能的后续行动提示""",
            
            "system_prompt_opening": """生成一个文字冒险游戏的开场。
        
要求：
- 设定一个有趣的世界背景
- 描述初始位置
- 给出前几个可能的操作建议
- 100-150字左右""",
            
            # UI Messages
            "game_status": "📊 游戏状态：",
            "story_events": "📝 故事事件数",
            "current_location": "📍 当前位置",
            "inventory_count": "🎒 物品数",
            "known_npcs": "🧑 已知NPC",
            
            "generating_opening": "🎮 正在生成开场故事...\n",
            "generating": "🤖 AI 生成中...\n",
            "generate_failed": "❌ 生成失败",
            "error_prefix": "❌ 错误",
            "success_checkmark": "✓",
            "player_action": "【你的操作】",
            "story_section": "【故事】",
            "auto_continue": "🔄 自动继续...\n",
            "game_saved": "✓ 游戏已保存到",
            "no_input": "⚠️ 请输入你的操作",
            "input_placeholder": "输入你的操作（例如：向前走，查看四周）",
            
            "button_execute": "▶️ 执行操作",
            "button_continue": "🔄 自动继续",
            "button_save": "💾 保存游戏",
            "button_load": "📂 加载游戏",
            
            "saved_games": "已保存的游戏",
            "no_saves": "还没有保存任何游戏",
            "load_failed": "加载失败",
            
            "interaction_title": "游戏交互",
            "your_action": "你的操作",
            "controls_hint": "游戏操作",
            
            "tips_title": "提示",
            "tips_gameplay": "**玩法**: 输入任何操作描述，游戏会根据你的操作生成故事",
            "tips_continue": "**自动继续**: 如果不输入操作，点\"自动继续\"让AI继续生成",
            "tips_save": "**保存游戏**: 随时点\"保存游戏\"存档当前进度",
            "tips_status": "**查看状态**: 执行相应代码查看当前游戏状态",
            "tips_cost": "**成本提示**: 每次AI调用都会消耗tokens，注意API使用成本",
            
            "api_key_missing": "❌ API密钥未设置",
            "api_key_hint": "检查API密钥是否正确设置在.env文件中",
            "local_model_hint": "如果使用本地模型，确保Ollama已启动",
        },
        
        "en": {
            # System prompts
            "system_prompt_story": """You are a story narrator for a text adventure game.

Your responsibilities:
1. Generate immersive story segments based on player actions
2. Strictly follow established world-building and character settings
3. Remember all previous events and player choices
4. Keep character names, NPCs, and item properties consistent
5. Make player actions actually impact story development
6. Each story segment should be 100-200 words with suspense

Story style:
- Use second person "you"
- Descriptive but not overly long
- Suggest possible follow-up actions at the end""",
            
            "system_prompt_opening": """Generate an opening for a text adventure game.
        
Requirements:
- Set an interesting world background
- Describe the initial location
- Suggest a few possible first actions
- Around 100-150 words""",
            
            # UI Messages
            "game_status": "📊 Game Status:",
            "story_events": "📝 Story Events",
            "current_location": "📍 Current Location",
            "inventory_count": "🎒 Items",
            "known_npcs": "🧑 Known NPCs",
            
            "generating_opening": "🎮 Generating opening story...\n",
            "generating": "🤖 Generating...\n",
            "generate_failed": "❌ Generation failed",
            "error_prefix": "❌ Error",
            "success_checkmark": "✓",
            "player_action": "【Your Action】",
            "story_section": "【Story】",
            "auto_continue": "🔄 Auto-continuing...\n",
            "game_saved": "✓ Game saved to",
            "no_input": "⚠️ Please input your action",
            "input_placeholder": "Enter your action (e.g., move forward, look around)",
            
            "button_execute": "▶️ Execute Action",
            "button_continue": "🔄 Auto Continue",
            "button_save": "💾 Save Game",
            "button_load": "📂 Load Game",
            
            "saved_games": "Saved Games",
            "no_saves": "No saved games yet",
            "load_failed": "Load failed",
            
            "interaction_title": "Game Interaction",
            "your_action": "Your Action",
            "controls_hint": "Game Controls",
            
            "tips_title": "Tips",
            "tips_gameplay": "**Gameplay**: Enter any action description, and the game will generate a story based on your action",
            "tips_continue": "**Auto Continue**: If you don't input an action, click \"Auto Continue\" to let AI continue the story",
            "tips_save": "**Save Game**: Save your progress anytime by clicking \"Save Game\"",
            "tips_status": "**View Status**: Run the corresponding code to see current game status",
            "tips_cost": "**Cost Note**: Each AI call consumes tokens, be mindful of API usage costs",
            
            "api_key_missing": "❌ API key not set",
            "api_key_hint": "Check if API key is correctly set in .env file",
            "local_model_hint": "If using a local model, ensure Ollama is running",
        }
    }
    
    @classmethod
    def get(cls, key: str, lang: str = None) -> str:
        """Get localized string
        
        Args:
            key: String key
            lang: Language code ("zh" or "en"), uses global LANGUAGE if None
        
        Returns:
            Localized string
        """
        if lang is None:
            lang = LANGUAGE
        
        if lang not in cls.STRINGS:
            lang = "en"  # Fallback to English
        
        return cls.STRINGS[lang].get(key, f"[Missing: {key}]")
    
    @classmethod
    def set_language(cls, lang: str) -> None:
        """Set global language
        
        Args:
            lang: "zh" for Chinese, "en" for English
        """
        global LANGUAGE
        if lang in cls.STRINGS:
            LANGUAGE = lang
        else:
            raise ValueError(f"Unsupported language: {lang}. Choose from {list(cls.STRINGS.keys())}")


# Convenience function
def _(key: str, lang: str = None) -> str:
    """Shorthand for LocalizationManager.get()
    
    Usage: print(_("generating"))
    """
    return LocalizationManager.get(key, lang)


# Export public API
__all__ = [
    "LANGUAGE",
    "LocalizationManager",
    "_"
]
