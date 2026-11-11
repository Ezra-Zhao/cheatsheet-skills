# cheatsheet-skills

Sixteen one-page cheatsheets, packaged as Agent Skills — so your AI coding agent stops guessing command flags and looks them up instead.

Each skill is one `SKILL.md`: 30 (or so) real commands for one tool, every one of them checked against the tool itself or its official docs before it went in. No filler, no scraped blog content. When your agent needs a `git`, `ffmpeg`, `kubectl` or `find` command, it reads the sheet and copies a command that actually runs.

中文版：[README.zh.md](README.zh.md)

## The skills

| Skill | What it covers | Source sheet |
|---|---|---|
| [git-cheatsheet](skills/git-cheatsheet/SKILL.md) | Daily git plus the emergency fixes: undo, reflog recovery, safe force-push | [git-cheatsheet](https://github.com/Ezra-Zhao/git-cheatsheet) |
| [docker-cheatsheet](skills/docker-cheatsheet/SKILL.md) | Containers, images, Compose, and why it keeps restarting | [docker-cheatsheet](https://github.com/Ezra-Zhao/docker-cheatsheet) |
| [ffmpeg-cheatsheet](skills/ffmpeg-cheatsheet/SKILL.md) | Convert, trim, compress, extract audio, subtitles, GIFs | [ffmpeg-cheatsheet](https://github.com/Ezra-Zhao/ffmpeg-cheatsheet) |
| [curl-cheatsheet](skills/curl-cheatsheet/SKILL.md) | HTTP requests, auth, JSON posts, downloads, API debugging | [curl-cheatsheet](https://github.com/Ezra-Zhao/curl-cheatsheet) |
| [jq-cheatsheet](skills/jq-cheatsheet/SKILL.md) | Filter, reshape and build JSON from the command line | [jq-cheatsheet](https://github.com/Ezra-Zhao/jq-cheatsheet) |
| [kubectl-cheatsheet](skills/kubectl-cheatsheet/SKILL.md) | Pod triage in the right order: describe, events, previous logs, rollback | [kubectl-cheatsheet](https://github.com/Ezra-Zhao/kubectl-cheatsheet) |
| [regex-cheatsheet](skills/regex-cheatsheet/SKILL.md) | Patterns that work, and where the flavors differ (grep/sed/Python/JS/PCRE) | [regex-cheatsheet](https://github.com/Ezra-Zhao/regex-cheatsheet) |
| [sql-cheatsheet](skills/sql-cheatsheet/SKILL.md) | SELECT to window functions, across MySQL, PostgreSQL and SQLite | [sql-cheatsheet](https://github.com/Ezra-Zhao/sql-cheatsheet) |
| [ssh-cheatsheet](skills/ssh-cheatsheet/SKILL.md) | Keys, config, tunnels, ProxyJump, file transfer | [ssh-cheatsheet](https://github.com/Ezra-Zhao/ssh-cheatsheet) |
| [find-xargs-cheatsheet](skills/find-xargs-cheatsheet/SKILL.md) | Find files by anything, then act on them safely with xargs | [find-xargs-cheatsheet](https://github.com/Ezra-Zhao/find-xargs-cheatsheet) |
| [awk-cheatsheet](skills/awk-cheatsheet/SKILL.md) | Fields, patterns and one-line recipes: sums, dedupe, group-bys, two-file joins | [awk-cheatsheet](https://github.com/Ezra-Zhao/awk-cheatsheet) |
| [grep-cheatsheet](skills/grep-cheatsheet/SKILL.md) | Search lines, trees and logs: recursion, regex flavors, context, exit codes, binary files, PCRE | [grep-cheatsheet](https://github.com/Ezra-Zhao/grep-cheatsheet) |
| [vim-cheatsheet](skills/vim-cheatsheet/SKILL.md) | Movement, operators, macros, and getting out with your work intact | [vim-cheatsheet](https://github.com/Ezra-Zhao/vim-cheatsheet) |
| [tmux-cheatsheet](skills/tmux-cheatsheet/SKILL.md) | Sessions, panes, copy mode, work that survives a closed terminal | [tmux-cheatsheet](https://github.com/Ezra-Zhao/tmux-cheatsheet) |
| [systemd-cheatsheet](skills/systemd-cheatsheet/SKILL.md) | systemctl, unit files, journalctl, timers | [systemd-cheatsheet](https://github.com/Ezra-Zhao/systemd-cheatsheet) |
| [terminal-superpowers-cheatsheet](skills/terminal-superpowers-cheatsheet/SKILL.md) | zoxide, fzf, fd, ripgrep, eza, bat and friends — the modern replacements | [terminal-superpowers-cheatsheet](https://github.com/Ezra-Zhao/terminal-superpowers-cheatsheet) |
| [adobe-free-alternatives-cheatsheet](skills/adobe-free-alternatives-cheatsheet/SKILL.md) | Free/open-source replacements for Adobe apps, with install commands | [adobe-free-alternatives-cheatsheet](https://github.com/Ezra-Zhao/adobe-free-alternatives-cheatsheet) |
| [desubscribe-cheatsheet](skills/desubscribe-cheatsheet/SKILL.md) | Swap paid SaaS for self-hosted open source, one Docker command each | [desubscribe-cheatsheet](https://github.com/Ezra-Zhao/desubscribe-cheatsheet) |

## Install

### Claude Code

```bash
git clone https://github.com/Ezra-Zhao/cheatsheet-skills.git
mkdir -p ~/.claude/skills
cp -r cheatsheet-skills/skills/* ~/.claude/skills/
```

Copy only the ones you want — each `skills/<name>/` folder is a complete, standalone skill. Claude Code picks them up automatically when a request matches the skill's description.

### Codex

```bash
git clone https://github.com/Ezra-Zhao/cheatsheet-skills.git
mkdir -p ~/.codex/skills
cp -r cheatsheet-skills/skills/* ~/.codex/skills/
```

The `SKILL.md` format is the shared Agent Skills format, so the same folders work in both.

## Just want to read them?

Every sheet also lives on the web, one page per real-world scenario: **[ezra-zhao.github.io/cheatsheet-pages](https://ezra-zhao.github.io/cheatsheet-pages/)** — and each source repo above carries the sheet with a Chinese, Spanish and Portuguese README.

## How this repo is built

- Format verified against the official examples in [anthropics/skills](https://github.com/anthropics/skills): YAML frontmatter with `name` and `description` only, directory name equal to `name`, body starting with the sheet itself.
- Each skill body is copied from its source repo's `CHEATSHEET.md` and machine-checked to be identical to it — commands cannot silently drift between the sheet and the skill. If a sheet gets fixed, the skill is rebuilt from it. Run the check yourself: `python3 scripts/verify_skills.py` (each body's SHA-256 is pinned in `scripts/skills-manifest.json` at build time).

## License

MIT — © 2026 Guangyi Zhao. See [LICENSE](LICENSE).
