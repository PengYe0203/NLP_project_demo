# 语言配置指南 | Language Configuration Guide

## 中文 (Chinese)

### 切换语言

项目支持中英文自动切换。修改环境变量或代码中的设置即可。

#### 方法 1: 修改代码（最简单）

编辑 `game/localization.py` 的第一行：

```python
# 中文模式
LANGUAGE = "zh"

# 英文模式（交付时改为）
LANGUAGE = "en"
```

#### 方法 2: 环境变量（推荐）

在 `.env` 文件中添加：

```bash
# 中文
GAME_LANGUAGE=zh

# 英文
GAME_LANGUAGE=en
```

#### 方法 3: Python代码中设置

```python
from game import LocalizationManager

# 切换到英文
LocalizationManager.set_language("en")

# 切换回中文
LocalizationManager.set_language("zh")
```

### 使用本地化字符串

在任何文件中使用本地化文本：

```python
from game.localization import _, LocalizationManager as L

# 简写方式
print(_("generating"))

# 完整方式
print(L.get("generating"))

# 指定语言
print(L.get("generating", lang="en"))
```

---

## English

### Switch Language

The project supports automatic Chinese-English switching. Just change the settings in the environment variable or code.

#### Method 1: Modify Code (Simplest)

Edit the first line in `game/localization.py`:

```python
# Chinese mode
LANGUAGE = "zh"

# English mode (change when delivering)
LANGUAGE = "en"
```

#### Method 2: Environment Variable (Recommended)

Add to `.env` file:

```bash
# Chinese
GAME_LANGUAGE=zh

# English
GAME_LANGUAGE=en
```

#### Method 3: Set in Python Code

```python
from game import LocalizationManager

# Switch to English
LocalizationManager.set_language("en")

# Switch back to Chinese
LocalizationManager.set_language("zh")
```

### Use Localized Strings

Use localized text in any file:

```python
from game.localization import _, LocalizationManager as L

# Shorthand
print(_("generating"))

# Full method
print(L.get("generating"))

# Specify language
print(L.get("generating", lang="en"))
```

---

## 支持的字符串键 | Supported String Keys

详见 `game/localization.py` 中的 `STRINGS` 字典。

所有UI文本、系统提示、错误消息等都已包含。

See the `STRINGS` dictionary in `game/localization.py` for all supported keys.

All UI text, system prompts, error messages, etc. are included.

---

## 开发工作流 | Development Workflow

1. **开发阶段** (中文调试)
   ```
   LANGUAGE = "zh"
   ```

2. **交付阶段** (改为英文)
   ```
   LANGUAGE = "en"
   ```

3. **提交代码**
   ```bash
   git add .
   git commit -m "Switch language to English for delivery"
   git push
   ```

完成！ | Done!
