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

**bo-new**
- [ ] Capture project ideas in a registry to choose to start on command.
- [ ] Scaffold new projects based on language and framework.
- [ ] Initialize Git.
- [ ] Create and link remote repos with configured namespace. 
- [ ] Register project locally with bo utilities for quick discovery and launch.

**bo-open**
- [X] Discover projects via fuzzy search.
- [X] Load configured tmuxp sessions to jump back into project development.
- [X] Show project information on fuzzy search (tmux session, git , github).
- [X] Start local or containerized contexts configured for the project.

**bo-clean**
- [ ] Maintain project registry by removing invalid entries.

**bo-status**
- [ ] Check synchronization between local and remote repositories.

**bo-help**
- [X] Display developer guides and tips (DEVELOPER.md) for each project.
- [ ] Discover markdown files via fuzzy search and open in man style viewer.

**bo-setup**
- [ ] Initialize project registry.
- [ ] Scan project roots for repositories to register.

### Documentation

README.md
[CONTRIBUTING.md](/CONTRIBUTING.md)

---

### License
This project is published under The Unlicense. The code is public domain; use it however you want.

Full text in [LICENSE.md](/LICENSE.md)
