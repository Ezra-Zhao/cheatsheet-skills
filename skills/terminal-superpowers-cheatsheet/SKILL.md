---
name: terminal-superpowers-cheatsheet
description: 'Use when the user wants modern terminal tools that upgrade classic Unix commands, or asks for a faster or friendlier alternative to cd, ls, cat, find or grep: zoxide, fzf, fd, ripgrep, eza, bat, starship, lazygit, tldr, btop, tmux and zellij. What each tool does, how to install it, and one command to try right away.'
---

# Terminal Superpowers — 2026 Cheatsheet

One page. Fourteen tools. Each entry tells you **what it does**, **how to install it**, and **one command to try right now**.

> 🌍 Read this project in your language: [中文](README.md) · [Español](README.es.md) · [Português](README.pt.md)

## Starter pack (macOS / Homebrew)

```bash
brew install zoxide fzf fd ripgrep eza bat starship lazygit tldr btop tmux zellij
```

On Debian/Ubuntu, most of these are also one `sudo apt install <name>` away.

---

## 🆕 New in 2026

### [cmux](https://github.com/manaflow-ai/cmux) — the terminal built for AI coding agents
A native macOS terminal (built on Ghostty) designed for running many AI agents in parallel: vertical tabs, per-agent notification rings so you can see which agent needs you, and a scriptable CLI.
```bash
brew tap manaflow-ai/cmux && brew install --cask cmux   # install
cmux notify "task done"                                 # try: ping yourself from an agent hook
```
🏷️ `#ai-agents` `#macos` · 🌐 https://cmux.com

### [yoinks](https://github.com/zoneboys/yoinks) — yoink any video from your terminal
Download videos from YouTube, X/Twitter, Instagram, Threads, TikTok and 1,800+ other sites without leaving the terminal. Paste a URL, pick a resolution (or audio-only mp3), done — no popups, no fake download buttons.
```bash
npm install -g yoinks   # install (needs Node 18+)
yoinks                  # try: paste any video URL when prompted
```
🏷️ `#media` `#download`

---

## 🧭 Navigation & search

### [zoxide](https://github.com/ajeetdsouza/zoxide) — a smarter `cd`
Remembers which directories you visit most and jumps to them in a few keystrokes. Type a fragment, land in the right place.
```bash
brew install zoxide                      # install
eval "$(zoxide init zsh)" >> ~/.zshrc    # hook into your shell
z proj                                   # try: jump to best match for "proj"
```
🏷️ `#navigation` `#productivity`

### [fzf](https://github.com/junegunn/fzf) — fuzzy finder for everything
Interactively filter files, shell history, and processes as you type. The fastest way to find anything you can name half of.
```bash
brew install fzf   # install
vim $(fzf)         # try: pick a file to open (or press Ctrl-R for history)
```
🏷️ `#search` `#fuzzy`

### [fd](https://github.com/sharkdp/fd) — a friendlier `find`
A fast `find` replacement with sane defaults, colorized output, and regex you can actually read.
```bash
brew install fd        # install
fd -e py config        # try: find all *.py files under config/
```
🏷️ `#search` `#files`

### [ripgrep](https://github.com/BurntSushi/ripgrep) — `grep`, rebuilt in Rust
Searches entire codebases in milliseconds, respects `.gitignore` by default, and prints results you can read.
```bash
brew install ripgrep   # install
rg "TODO" src/         # try: find every TODO in src/
```
🏷️ `#search` `#code`

---

## 🖥️ Multiplexing & prompt

### [tmux](https://github.com/tmux/tmux) — the classic terminal multiplexer
Split panes, persistent sessions, detach and reattach over SSH. If your work lives on remote servers, this is non-negotiable.
```bash
brew install tmux      # macOS — or: sudo apt install tmux
tmux new -s work        # try: new session named "work" (Ctrl-b % splits, Ctrl-b d detaches)
```
🏷️ `#multiplexer` `#ssh` `#remote`

### [zellij](https://github.com/zellij-org/zellij) — tmux with training wheels (in a good way)
A modern terminal workspace: discoverable keybindings, layouts, floating panes, and sessions that survive restarts. Easier to learn than tmux, just as powerful.
```bash
brew install zellij   # install
zellij -s dev         # try: start a session named "dev"
```
🏷️ `#multiplexer` `#workspace` · 🌐 https://zellij.dev

### [starship](https://github.com/starship/starship) — a prompt that tells you things
A minimal, fast, endlessly customizable shell prompt: git branch and status, language versions, command duration — right where you look.
```bash
brew install starship                    # install
eval "$(starship init zsh)" >> ~/.zshrc  # hook into your shell, then cd into any git repo
```
🏷️ `#prompt` `#customization` · 🌐 https://starship.rs

---

## 📄 File viewing

### [eza](https://github.com/eza-community/eza) — a modern `ls`
Colors, icons, git status, and tree view in a single fast binary. The maintained successor to `exa`.
```bash
brew install eza          # install
eza -la --icons --git     # try: long listing with icons and git status
```
🏷️ `#files` `#listing` · 🌐 https://eza.rocks

### [bat](https://github.com/sharkdp/bat) — `cat` with syntax highlighting
Pipes code through highlighting, line numbers, and git markers. Once you use it, plain `cat` feels broken.
```bash
brew install bat   # install
bat main.py        # try: view any source file
```
🏷️ `#files` `#viewing`

---

## 🛠️ Dev workflow

### [lazygit](https://github.com/jesseduffield/lazygit) — git, without the memorization
A keyboard-driven terminal UI for git: stage individual hunks, interactive rebase, resolve conflicts, manage branches — all without leaving the keyboard.
```bash
brew install lazygit   # install
lazygit                # try: run it inside any git repo
```
🏷️ `#git` `#tui`

### [tldr](https://github.com/tldr-pages/tldr) — man pages you'll actually read
Community-maintained cheat sheets for commands: short, example-first, no archaeology required.
```bash
brew install tldr   # install, then: tldr --update
tldr tar            # try: finally understand tar's flags
```
🏷️ `#learning` `#reference`

---

## 📊 Monitoring

### [btop](https://github.com/aristocratos/btop) — resource monitor, but beautiful
CPU, memory, disks, network, and processes in one gorgeous terminal UI. `top` for people with eyes.
```bash
brew install btop   # macOS — or: sudo apt install btop
btop                # try: that's it, just look at it
```
🏷️ `#monitoring` `#ops`

---

## Contributing

Found a better tool, a wrong command, or a missing translation? Pull requests are welcome — please keep entries to the format above (what / install / try / tags) and verify every link before submitting.

## License

MIT © 2026 Guangyi Zhao. See [LICENSE](LICENSE).
