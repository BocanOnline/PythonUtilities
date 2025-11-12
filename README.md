# PythonUtilities — The Bocan Online Developer Toolkit

A unified command-line toolkit for creating, discovering, and managing 
Bocan Online and Bocan Studio projects.

---

### Overview

**PythonUtilities** is a modular CLI system built in **Python**, integrating 
with **tmuxp** to manage project contexts and development environments.

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

### Planned Utilities

**bo-new**
- Scaffold new projects based on language and framework.
- Initialize Git.
- Create and link remote repos with configured namespace. 
- Register project locally with bo utilities for quick discovery and launch.

**bo-open**
- Discover projects via fuzzy search.
- Load configured tmuxp sessions to jump back into project development.
- Start local or containerized contexts configured for the project.

**bo-clean**
- Maintain project registry by removing invalid entries.

**bo-status**
- Check synchronization between local and remote repositories.

**bo-help**
- Display developer guides and tips (DEVELOPER.md) for each project.
- Discover markdown files via fuzzy search and open in man style viewer.

**bo-setup**
- Initialize project registry.
- Scan project roots for repositories to register.

**bo-switch**
- Discover tmux sessions via fuzzy search.
- Quickly switch between active tmux sessions.
- Clean up or end tmux sessions.

---

### Architecture Direction

- **Language:** Python  
- **Session Management:** tmuxp  
- **Design:** small, composable commands in a single monorepo  
- **Configuration:** stored in `~/.config/bo/`  
- **Brand:** *Bocan Online* — minimal, developer-oriented, GNU-inspired

---

### Documentation

README.md
DEVELOPER.md

---

### License

To be determined — likely MIT or GPLv3 depending on ecosystem compatibility.
