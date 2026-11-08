# cheatsheet-skills · 速查表技能包

十六张一页速查表，打包成 Agent Skills——让您的 AI 编程助手别再凭感觉编命令参数，先查表再动手。

每个 skill 就是一个 `SKILL.md`：一个工具约 30 条真命令，每条都对着工具本身或官方文档核过才收进来。没有凑数内容，没有从博客上扒的二手货。Agent 需要 `git`、`ffmpeg`、`kubectl`、`find` 命令时，读表、抄一条能直接跑的。

English: [README.md](README.md)

## 技能清单

| Skill | 内容 | 源仓 |
|---|---|---|
| [git-cheatsheet](skills/git-cheatsheet/SKILL.md) | 日常 git＋救急：撤销、reflog 找回、安全强推 | [git-cheatsheet](https://github.com/Ezra-Zhao/git-cheatsheet) |
| [docker-cheatsheet](skills/docker-cheatsheet/SKILL.md) | 容器、镜像、Compose，以及容器为什么老重启 | [docker-cheatsheet](https://github.com/Ezra-Zhao/docker-cheatsheet) |
| [ffmpeg-cheatsheet](skills/ffmpeg-cheatsheet/SKILL.md) | 转格式、剪切、压缩、抽音频、字幕、GIF | [ffmpeg-cheatsheet](https://github.com/Ezra-Zhao/ffmpeg-cheatsheet) |
| [curl-cheatsheet](skills/curl-cheatsheet/SKILL.md) | HTTP 请求、认证、发 JSON、下载、调 API | [curl-cheatsheet](https://github.com/Ezra-Zhao/curl-cheatsheet) |
| [jq-cheatsheet](skills/jq-cheatsheet/SKILL.md) | 在命令行里过滤、重塑、拼装 JSON | [jq-cheatsheet](https://github.com/Ezra-Zhao/jq-cheatsheet) |
| [kubectl-cheatsheet](skills/kubectl-cheatsheet/SKILL.md) | 排障顺序：describe、events、上一个容器的日志、回滚 | [kubectl-cheatsheet](https://github.com/Ezra-Zhao/kubectl-cheatsheet) |
| [regex-cheatsheet](skills/regex-cheatsheet/SKILL.md) | 能用的正则模式，以及各家方言差异（grep/sed/Python/JS/PCRE） | [regex-cheatsheet](https://github.com/Ezra-Zhao/regex-cheatsheet) |
| [sql-cheatsheet](skills/sql-cheatsheet/SKILL.md) | 从 SELECT 到窗口函数，MySQL/PostgreSQL/SQLite 通用 | [sql-cheatsheet](https://github.com/Ezra-Zhao/sql-cheatsheet) |
| [ssh-cheatsheet](skills/ssh-cheatsheet/SKILL.md) | 密钥、配置文件、隧道、ProxyJump、传文件 | [ssh-cheatsheet](https://github.com/Ezra-Zhao/ssh-cheatsheet) |
| [find-xargs-cheatsheet](skills/find-xargs-cheatsheet/SKILL.md) | 按各种条件找文件，再用 xargs 安全地批量处理 | [find-xargs-cheatsheet](https://github.com/Ezra-Zhao/find-xargs-cheatsheet) |
| [awk-cheatsheet](skills/awk-cheatsheet/SKILL.md) | 字段、模式与单行配方：求和、去重、分组汇总、双文件 join | [awk-cheatsheet](https://github.com/Ezra-Zhao/awk-cheatsheet) |
| [vim-cheatsheet](skills/vim-cheatsheet/SKILL.md) | 移动、操作符、宏，以及带着成果全身而退 | [vim-cheatsheet](https://github.com/Ezra-Zhao/vim-cheatsheet) |
| [tmux-cheatsheet](skills/tmux-cheatsheet/SKILL.md) | 会话、窗格、复制模式，关了终端活还在 | [tmux-cheatsheet](https://github.com/Ezra-Zhao/tmux-cheatsheet) |
| [systemd-cheatsheet](skills/systemd-cheatsheet/SKILL.md) | systemctl、unit 文件、journalctl、定时器 | [systemd-cheatsheet](https://github.com/Ezra-Zhao/systemd-cheatsheet) |
| [terminal-superpowers-cheatsheet](skills/terminal-superpowers-cheatsheet/SKILL.md) | zoxide、fzf、fd、ripgrep、eza、bat 等现代替代品 | [terminal-superpowers-cheatsheet](https://github.com/Ezra-Zhao/terminal-superpowers-cheatsheet) |
| [adobe-free-alternatives-cheatsheet](skills/adobe-free-alternatives-cheatsheet/SKILL.md) | Adobe 各软件的免费/开源替代，带安装命令 | [adobe-free-alternatives-cheatsheet](https://github.com/Ezra-Zhao/adobe-free-alternatives-cheatsheet) |
| [desubscribe-cheatsheet](skills/desubscribe-cheatsheet/SKILL.md) | 付费 SaaS 换自托管开源，一条 Docker 命令一个 | [desubscribe-cheatsheet](https://github.com/Ezra-Zhao/desubscribe-cheatsheet) |

## 安装

### Claude Code

```bash
git clone https://github.com/Ezra-Zhao/cheatsheet-skills.git
mkdir -p ~/.claude/skills
cp -r cheatsheet-skills/skills/* ~/.claude/skills/
```

想要哪几个就拷哪几个——每个 `skills/<名字>/` 文件夹都是完整独立的 skill。请求与某个 skill 的描述对上时，Claude Code 会自动用它。

### Codex

```bash
git clone https://github.com/Ezra-Zhao/cheatsheet-skills.git
mkdir -p ~/.codex/skills
cp -r cheatsheet-skills/skills/* ~/.codex/skills/
```

`SKILL.md` 是通用的 Agent Skills 格式，同一批文件夹两边都能用。

## 只想看，不想装？

每张表在网上都有网页版，一个真实场景一页：**[ezra-zhao.github.io/cheatsheet-pages](https://ezra-zhao.github.io/cheatsheet-pages/)**；每个源仓里还有中文、西语、葡语 README。

## 这个仓是怎么做的

- 格式对着官方仓 [anthropics/skills](https://github.com/anthropics/skills) 的真实例子验过：YAML frontmatter 只有 `name` 和 `description`、目录名与 `name` 一致、正文就是速查表本身。
- 每个 skill 的正文从源仓的 `CHEATSHEET.md` 复制，并用脚本核对到逐字一致——命令不会在表和 skill 之间悄悄跑偏。源表改了，skill 从源表重建。校验可自跑：`python3 scripts/verify_skills.py`（正文 SHA-256 已钉在 `scripts/skills-manifest.json`）。

## 许可

MIT — © 2026 Guangyi Zhao。见 [LICENSE](LICENSE)。
