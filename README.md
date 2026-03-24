# NLP Project Demo: AI-Powered Text Adventure Game

这是一个基于AI生成内容的文字冒险游戏项目。玩家可以随时进行任何操作，也可以什么都不做让AI继续生成故事。

![Version](https://img.shields.io/badge/version-0.1.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)

## 项目特色

- 🎮 **自由交互** - 玩家可在任何时刻进行任意操作或选择自动继续
- 🤖 **多个AI后端** - 支持OpenAI、Claude、本地模型等
- 💾 **游戏存档** - 支持保存/读取游戏进度
- 🎯 **上下文管理** - 防止AI遗忘故事背景
- 📊 **Jupyter演示** - 交互式notebook界面

## 项目结构

```
NLP_project_demo/
├── game/                    # 核心游戏模块
│   ├── __init__.py
│   ├── story_generator.py   # AI故事生成器
│   └── game_engine.py       # 游戏引擎和状态管理
├── output/                  # 游戏存档目录
├── demo.ipynb              # 交互演示（Jupyter Notebook）
├── requirements.txt        # 项目依赖
├── .gitignore
└── README.md
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置API密钥

创建 `.env` 文件：

```bash
# OpenAI
OPENAI_API_KEY=sk-xxx

# Claude (可选)
ANTHROPIC_API_KEY=sk-ant-xxx
```

### 3. 运行演示

#### 选项A: Jupyter Notebook
```bash
jupyter notebook demo.ipynb
```

#### 选项B: 直接Python脚本
```python
from game import create_generator, TextAdventureGame

# 创建生成器（选择后端）
generator = create_generator(backend="openai")

# 初始化游戏
game = TextAdventureGame(generator)

# 开始游戏
print(game.initialize_story())

# 玩家操作
while True:
    action = input("\n你的操作：")
    if action.lower() in ["退出", "exit", "quit"]:
        game.save_game()
        break
    print(game.process_action(action))
```

## 支持的AI后端

### OpenAI
```python
from game import create_generator

generator = create_generator(
    backend="openai",
    model_name="gpt-4o-mini"  # 或 gpt-3.5-turbo
)
```

### Anthropic Claude
```python
generator = create_generator(
    backend="claude",
    model_name="claude-3-5-sonnet-20241022"
)
```

### 本地模型（Ollama）
需要先启动Ollama服务：
```bash
ollama run llama3
```

然后：
```python
generator = create_generator(
    backend="local",
    model_name="llama3",
    api_url="http://localhost:11434"
)
```

## API使用成本参考

| 模型 | 成本(per 1M tokens) | 推荐 |
|------|-------------------|------|
| GPT-3.5-turbo | $0.5 | ✓ 入门 |
| GPT-4o-mini | $0.15 | ✓✓ 推荐 |
| GPT-4o | $15 | ✓✓✓ 最佳 |
| Claude 3.5 Sonnet | $3 | ✓✓ 优质 |
| 本地模型 | 免费 | ✓ 隐私优先 |

## 主要模块说明

### StoryGenerator (game/story_generator.py)
- `OpenAIStoryGenerator` - OpenAI API集成
- `ClaudeStoryGenerator` - Claude API集成
- `LocalStoryGenerator` - 本地模型集成（Ollama等）
- `create_generator()` - 工厂函数快速创建生成器

### GameEngine (game/game_engine.py)
- `GameState` - 管理游戏状态（位置、物品、NPC等）
- `ContextManager` - 管理故事上下文，防止遗忘
- `TextAdventureGame` - 主游戏引擎

## 游戏流程

```
初始化 → 生成开场 → [等待玩家操作/自动继续] → 生成故事 → 更新状态 → 循环
```

## 功能特性

### 1. 灵活的玩家交互
- `/continue` 或空操作 - 自动继续故事
- `/save` - 保存游戏
- `/load [file]` - 加载存档
- `/status` - 查看游戏状态
- `/quit` - 退出游戏

### 2. 上下文一致性
- 自动提取并记忆游戏关键信息（位置、物品、NPC）
- 防止上下文过长（智能历史裁剪）
- 强制提醒重要世界观信息

### 3. 游戏存档
- JSON格式存档
- 支持随时保存/加载
- 完整保留游戏历史

## 常见问题

### Q: 需要付费吗？
A: 使用API需要付费（可控制）。本地模型完全免费但需要较好硬件。

### Q: 如何防止AI遗忘？
A: 项目已内置ContextManager，自动管理上下文。关键信息会在提示词中反复强调。

### Q: 支持离线运行吗？
A: 支持！使用本地模型（Ollama）可完全离线。

### Q: 怎样编辑故事生成的"性格"？
A: 修改 `story_generator.py` 中的 `_create_system_prompt()` 方法。

## 扩展建议

- [ ] 使用Named Entity Recognition (NER) 改进事实提取
- [ ] 添加游戏难度/剧情分支系统
- [ ] 实现角色系统和技能树
- [ ] 支持多玩家/联网
- [ ] 添加语音/TTS输出
- [ ] 集成向量数据库存储长期记忆

## 作者

PolyU NLP Course Project Demo

## 许可证

MIT License
