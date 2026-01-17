# dialog-yaml

[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/) [![aiogram-dialog 2.4.0](https://img.shields.io/badge/aiogram--dialog-2.4.0-green.svg)](https://pypi.org/project/aiogram-dialog/) [![Coverage Status](https://img.shields.io/badge/coverage-unknown-red.svg)](https://pypi.org/project/dialog-yaml/)

---

> ⚠️ **WARNING**: This library is experimental. The author is not responsible for any problems that may arise from its use.

A Python library that enables building [aiogram-dialog](https://github.com/tishka17/aiogram_dialog) applications using YAML configuration files. This library simplifies the creation of Telegram bots with complex dialog flows by allowing developers to define dialogs, windows, and widgets declaratively in YAML format.

## 📖 Overview

The `dialog-yaml` library provides a `DialogYAMLBuilder` class that reads YAML configuration files and converts them into functional aiogram dialogs. This approach allows for rapid prototyping and easier management of complex dialog structures without writing extensive Python code.

## ✨ Features

### 📝 Declarative Dialog Definition

Define dialogs, windows, and widgets using YAML files

### 🔧 Modular Structure

Support for including separate YAML files using `!include` directive

### 📌 YAML Anchors

Support for YAML anchors (`&`) and references (`*`) to avoid duplication

### 🎛️ Built-in Widgets

Support for various aiogram-dialog widgets including:

- Text elements
- Keyboard widgets
- Calendar widgets
- Selection widgets
- Scrolling widgets
- Counter widgets
- Media widgets
- other...

### ⚙️ Custom Functions

Extensible function registry for custom business logic

### 🧩 Custom Models

Ability to register custom widget models

### 🗂️ State Management

Automatic generation and management of FSM states from YAML configuration

### 🎚️ Flexible Configuration

Support for custom states groups and models

## 📦 Installation

For installation use pip:

```bash
pip install dialog-yaml
```

Or if you use uv (recommended):

```bash
uv pip install dialog-yaml
```

## 🧰 Requirements

- Python >= 3.13
- aiogram >= 3.24.0
- aiogram-dialog >= 2.4.0
- pydantic >= 2.12.5
- PyYAML >= 6.0.3

## 👤 Usage (for Users)

### ⚙️ Basic Setup

Here's a basic example of how to use the library:

```python
from aiogram import Router
from dialog_yaml import DialogYAMLBuilder

# Build the dialog from a YAML file
dy_builder = DialogYAMLBuilder.build(
    yaml_file_name="main.yaml",
    yaml_dir_path="path/to/yaml/files",
    router=Router(),
)

# Access the configured router
router = dy_builder.router
```

### 📄 YAML Structure

The basic structure of a dialog YAML file:

```yaml
---
dialogs:
  DialogGroupName:  # This will become a StatesGroup name
    launch_mode: ROOT  # Optional launch mode
    windows:
      STATE_NAME:  # This will become a State name
        widgets:
          - text: "Hello, World!"
          - button:
              text: "Click me"
              id: click_btn
              on_click: my_function
...
```

### ⚙️ Using Custom Functions

You can define custom functions in your Python code and reference them in YAML files. Here's how to register and use custom functions:

**Python code:**

```python
from aiogram import Router
from aiogram_dialog import DialogManager
from dialog_yaml import DialogYAMLBuilder, FuncsRegistry

# Define your custom function
async def my_custom_function(dialog_manager: DialogManager, callback_data: str):
    # Your custom logic here
    print(f"Callback data: {callback_data}")
    # You can access dialog data via dialog_manager
    await dialog_manager.show()

# Create a function registry and register your function
funcs_registry = FuncsRegistry()
funcs_registry.register("my_function", my_custom_function)

# Build the dialog with custom functions
dy_builder = DialogYAMLBuilder.build(
    yaml_file_name="main.yaml",
    yaml_dir_path="path/to/yaml/files",
    router=Router(),
)
```

**YAML file:**

```yaml
---
dialogs:
  Menu:
    windows:
      MAIN:
        widgets:
          - text: "Welcome to our bot!"
          - button:
              text: "Click me"
              id: click_btn
              on_click: my_function  # This refers to the function registered in Python
...
```

### 📥 Using Custom Functions with Parameters

You can also pass parameters to your custom functions:

**Python code:**

```python
async def greet_user(dialog_manager: DialogManager, callback_data: str):
    # Extract data from callback_data if needed
    user_id = dialog_manager.event.from_user.id
    await dialog_manager.show()  # Refresh the dialog

async def navigate_to_settings(dialog_manager: DialogManager, callback_data: str):
    # Navigate to a different state
    await dialog_manager.switch_to(State.SETTINGS)

# Register the functions
funcs_registry = FuncsRegistry()
funcs_registry.register("greet_user", greet_user)
funcs_registry.register("go_to_settings", navigate_to_settings)
```

**YAML file:**

```yaml
---
dialogs:
  Menu:
    windows:
      MAIN:
        widgets:
          - text: "Main Menu"
          - button:
              text: "Greet Me"
              id: greet_btn
              on_click: greet_user
          - start:
              text: "Settings"
              id: settings_btn
              state: Menu:SETTINGS
              on_click: go_to_settings
...
```

### 🔄 How Custom Functions Are Interpreted

When the dialog-yaml library processes your YAML files:

1. It scans for properties like `on_click`, `on_process_result`, `on_selected`, etc., that contain function names
2. It looks up these function names in the internal function registry
3. When the corresponding widget event occurs, it calls the registered Python function
4. The function receives the `dialog_manager` object and `callback_data` as parameters

This allows you to implement complex business logic in Python while keeping the UI structure in YAML files.

### 📌 Using YAML Anchors

To avoid duplication in YAML files, you can use anchor data:

```yaml
---
anchors:
  back_button: &back
    id: back
    text: "Back"
    state: Menu:MAIN
  multi_select: &multi_select_config
    checked: {val: "✓ {item[0]}", formatted: true}
    unchecked: {val: "{item[0]}", formatted: true}
    id: ms
    items: products
    item_id_getter: 1

windows:
  MAIN:
    widgets:
      - text: "Main Menu"
      - button:
          text: "To Settings"
          id: settings
          state: Settings:MAIN
  SETTINGS:
    widgets:
      - text: "Settings"
      - multi_select: *multi_select_config
      - switch_to: *back
...
```

### 📁 Including External YAML Files

The library supports including external YAML files using the `!include` directive:

**main.yaml:**

```yaml
---
dialogs:
  Menu: !include menu.yaml
  Settings: !include settings.yaml
...
```

**menu.yaml:**

```yaml
---
launch_mode: ROOT
windows:
  MAIN:
    widgets:
      - text: "Main Menu"
      - start:
          text: "Go to Settings"
          id: settings_btn
          state: Settings:MAIN
...
```

## 👨‍💻 Development (for Developers)

### 📦 Installation for Development

If you want to contribute to the development of the library, install dependencies with uv:

```bash
uv sync
```

Or with pip:

```bash
pip install -e .
pip install -r requirements.txt
```

### 🧱 Dependencies

All project dependencies are fixed in the [requirements.txt](requirements.txt) file and in the `[project.dependencies]` section of `pyproject.toml`.

### 🛠️ Used Tools

🐍 **uv** - main package manager for the project
🧼 **Ruff** - code formatter and linter
🧪 **pytest** - for running tests
📦 **setuptools** - for package building

## 🏗️ Project Structure

The library follows a modular structure:

- `src/core.py`: Contains the main `DialogYAMLBuilder` class
- `src/reader.py`: Handles YAML file reading with include support
- `src/models/`: Contains model definitions for different dialog components
  - `base.py`: Base model classes
  - `dialog.py`: Dialog model
  - `window.py`: Window model
  - `widgets/`: Various widget models
  - `funcs/`: Function-related models
- `src/middleware.py`: Dialog YAML middleware
- `src/states.py`: State management utilities

## 📚 Examples

See the [examples/mega](examples/mega/) directory for a comprehensive example that demonstrates:

- Multiple dialog groups
- Different widget types
- Custom functions
- State transitions
- YAML includes
- Using anchor data

To run the example:

1. Create a `.env` file with your bot token and log level:

   ```
   MEGA_BOT_TOKEN=your_telegram_bot_token
   MEGA_BOT_LOG_LEVEL=INFO
   ```

2. Run the example:

   ```bash
   # If using uv (recommended)
   PYTHONPATH=. uv run examples/mega/bot.py
   
   # Or if using python directly
   PYTHONPATH=. python examples/mega/bot.py
   ```

> **Note**: The `PYTHONPATH=.` is required to ensure Python can correctly resolve the module imports when running the example.

## ⌨️ Available Commands

This project uses a Makefile for common tasks:

💡 `make help` - Show available commands
🧼 `make format` - Format code with Ruff
🔍 `make check` - Run code quality checks
🧪 `make test` - Run tests
📊 `make test-cov` - Generate test coverage report
📈 `make test-html` - Generate HTML test coverage report
🤖 `make mega-bot` - Run mega bot example

## 🧪 Testing

Run the test suite:

```bash
make test
# or
python -m pytest tests/
```

## 📦 Packaging and Publishing

To package and publish the library, follow these steps:

1. Make sure you have the necessary tools installed:

   ```bash
   pip install build twine
   # or using uv
   uv pip install build twine
   ```

2. Update the version in `pyproject.toml` before publishing

3. Build distributions:

   ```bash
   python -m build
   # or using uv
   uv run python -m build
   ```

4. Upload the package to PyPI:

   ```bash
   python -m twine upload dist/*
   ```

The `.python-version` file contains the Python version recommended for development. It does not affect package packaging but informs other developers which Python version to use when working with the project.

## 📄 License

This project is licensed under the terms specified in the [LICENSE](LICENSE) file.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.
