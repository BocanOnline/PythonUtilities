# PythonUtilities — The Bocan Online Developer Toolkit

A unified command-line toolkit for creating, discovering, and managing 
Bocan Online and Bocan Studio projects.

---

### Overview

**PythonUtilities** is a modular CLI system built in **Python**, integrating with **tmuxp** to manage project contexts and development environments.

It brings together project creation, discovery, launching, and maintenance 
into a cohesive personal workflow — a minimal, text-based "developer OS" 
inspired by GNU philosophy and Unix composability.

---

### Goals

- Simplify creation and setup of new projects.
- Launch local or containerized environments with tmuxp.
- Maintain a clean and accurate project registry.
- Keep all configuration declarative and portable.
- Develop a consistent, branded toolchain under **Bocan Online**.
- Make utilities portable to other Linux/macOS machines.

---

## Installation

### 1. Create a global virtual environment
It is recommended to install Bocan Utilities into a dedicated venv so the commands are available system-wide:

```bash
python3 -m venv ~/.venvs/bocan
```

### 2. Activate the environment
```bash
source ~/.venvs/bocan/bin/activate
```

### 3. Install in editable mode
Install the utilities so updates take effect immediately when developing:

```bash
pip install -e /path/to/PythonUtilities
```

### 4. Add the venv to your PATH
Append the following line to your `~/.zshrc`:

```bash
export PATH="$HOME/.venvs/bocan/bin:$PATH"
```

Then reload:

```bash
source ~/.zshrc
```

### 5. Deactivate the environment
The environment does not need to remain active to use the commands.

```bash
deactivate
```

### 6. Verify installation
```bash
bo-open
bo-help
bo-switch
```

These commands should now be available globally, without activating the environment again.

---

### Planned Utilities

**bo-help**
- [X] Display developer guides and tips (.bocan.yaml) for each project.

**bo-new**
- [ ] Capture project ideas in a registry to choose to start on command.
- [ ] Scaffold new projects based on language and framework (recipe.yaml).
- [ ] Initialize Git.
- [ ] Create and link remote repos with configured namespace. 
- [ ] Register project locally with bo utilities for quick discovery and launch.

**bo-open**
- [X] Discover projects via fuzzy search.
- [X] Load configured tmuxp sessions to jump back into project development.
- [ ] Show project information on fuzzy search (tmux session, git , github).
- [X] Start local or containerized contexts configured for the project.

**bo-register**
- [ ] Initialize project registry (first time run).
- [ ] Add idea to backlog file.
- [ ] Ask questions to flesh idea out.
- [ ] Flag to run bo-new with the same command.

**bo-update**
- [ ] Run in the background to keep project registry data up-to-date.
- [ ] Maintain project registry by removing invalid entries.
- [ ] Check if project tmux session is currently open.
- [ ] Check git status.
- [ ] Check synchronization between local and remote repositories.

### Documentation

README.md

---

### License
This project is published under The Unlicense. The code is public domain; use it however you want.

Full text in [LICENSE.md](/LICENSE.md)
