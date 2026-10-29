---
name: tmux-cheatsheet
description: 'Use when the user needs tmux commands: creating and attaching sessions, windows and panes, splitting and resizing, copy mode and scrollback search, the tmux.conf file, and keeping work alive after the terminal closes.'
---

# tmux Cheatsheet — Sessions, Windows, Panes & Copy Mode That Actually Work

One page. Thirty entries: sessions, windows, panes, copy mode and buffers, the `~/.tmux.conf` settings worth having, and scripting hooks. Each entry tells you **what it does**, **a command you can copy-paste**, and **tags**. No made-up keys — every CLI command below was run for real against tmux 3.4 in detached test sessions (results checked with `capture-pane` and the `list-*` commands), every prefix-key binding was checked against the default binding table printed by `tmux list-keys`, and the config examples were loaded with `tmux -f` and read back with `show-options`.

**The prefix key:** tmux's default prefix is **Ctrl-b**. Everywhere below, `prefix` means Ctrl-b — so "`prefix` c" means: press Ctrl-b, let go, then press c. Almost everything interactive in tmux starts with the prefix.

> 🌍 Read this project in your language: [中文](README.md) · [Español](README.es.md) · [Português](README.pt.md)

Docs: https://github.com/tmux/tmux/wiki

---

## 🖥️ Sessions — work that survives a closed terminal

A session is a whole workspace (windows + panes) that lives on the tmux server, not in your terminal. Close the terminal, lose your SSH connection, reboot your laptop — the session keeps running on the machine until you kill it or the machine reboots.

### `tmux new -s name` — create a named session
```bash
tmux new -s work        # create a session called "work" and attach to it
tmux new                # unnamed sessions get numbers: 0, 1, 2, ...
```
Named sessions are the whole point — you reattach by name hours later, from any terminal.
🏷️ `#session` `#basics` `#must-know`
### `tmux ls` + `tmux attach -t` — list sessions, reattach
```bash
tmux ls                     # list sessions (ls is the built-in alias of list-sessions)
tmux attach -t work         # reattach to the session called "work"
tmux a -t work              # same thing — tmux accepts "a" as a short form of attach
```
🏷️ `#session` `#basics` `#must-know`
### `prefix d` — detach: leave everything running
```bash
# inside tmux: press prefix (Ctrl-b), then d
tmux detach-client          # the same detach, run as a command
tmux detach-client -s work  # detach every client attached to session "work"
```
Detach is not exit: the shell, the build, the long-running job — all keep going inside the session. This is the feature that makes tmux worth learning; everything else is organisation.
🏷️ `#session` `#detach` `#must-know`
### `prefix $` — rename the session
```bash
# inside tmux: prefix $ prompts for a new name, pre-filled with the current one
tmux rename-session -t work main   # rename "work" to "main" from the command line
```
Rename early: three sessions called `0`, `1` and `2` tell you nothing a day later.
🏷️ `#session` `#rename`
### `tmux kill-session -t` — end one session for good
```bash
tmux kill-session -t work   # ⚠️ destroys the session AND every window, pane and
                            # process inside it — unsaved work in there is gone
# inside tmux: prefix s opens the session tree (choose-tree) —
# arrow keys to pick a session, Enter to jump to it
```
🏷️ `#session` `#kill` `#danger`

---

## 🧩 Windows — tabs inside a session

### `prefix c` — new window, `prefix ,` — rename it
```bash
# inside tmux: prefix c creates a window; prefix , prompts for its name
tmux rename-window -t work:1 logs   # the same rename from the command line
```
Windows are numbered from 0 by default (`base-index` can change that — see the config section).
🏷️ `#window` `#basics`
### Switching windows — `prefix n` / `p`, digits, list
```bash
# prefix n  → next window        prefix p  → previous window
# prefix 0 … prefix 9  → jump straight to window number 0–9
# prefix w  → window list (choose-tree) — arrows + Enter
tmux select-window -t work:2      # the same jump from the command line
```
🏷️ `#window` `#navigation` `#must-know`
### `prefix &` — kill the current window
```bash
# inside tmux: prefix & asks "kill-window <name>? (y/n)" — press y to confirm
tmux kill-window -t work:2        # no confirmation from the command line
# ⚠️ killing a window ends every pane and process inside it, shell included
```
🏷️ `#window` `#kill` `#danger`
### `tmux new-window` — create a window from the command line
```bash
tmux new-window -t work -n logs              # new window named "logs" in session "work"
tmux new-window -t work:5 -n build           # …at index 5 (the index must be free)
tmux new-window -t work -n tail -c /var/log 'tail -f app.log'
# -c sets the start directory; a trailing shell command runs in the new window
# (the window lives as long as that command runs)
```
🏷️ `#window` `#cli` `#scripting`
### `swap-window` / `move-window` — reorder windows
```bash
tmux swap-window -s work:1 -t work:3   # swap the positions of windows 1 and 3
tmux move-window -s work:1 -t work:5   # move window 1 to index 5 (must be empty)
# inside tmux: prefix . prompts for a target index and moves the current window there
```
🏷️ `#window` `#organise`

---

## 📐 Panes — splits inside a window

### `prefix %` / `prefix "` — split side-by-side / top-and-bottom
```bash
# prefix %   → vertical divider: two panes side by side (left | right)
# prefix "   → horizontal divider: two panes stacked (top / bottom)
# memory hook: % has two halves next to each other; " sits on one line,
# so the cut runs along that line and stacks the panes
tmux split-window -h    # the command-line form of prefix %  (-h = side by side)
tmux split-window -v    # the command-line form of prefix "  (-v = stacked)
```
🏷️ `#pane` `#split` `#must-know`
### Moving between panes — arrows, `prefix o`, `prefix q`
```bash
# prefix ← ↑ ↓ →  → move focus to the pane in that direction
# prefix o        → cycle to the next pane
# prefix q        → flash a number on each pane; press that number to jump there
tmux select-pane -t work:0.1   # focus pane 1 of window 0, from the command line
```
🏷️ `#pane` `#navigation` `#must-know`
### `prefix z` — zoom a pane full-screen (and back)
```bash
# prefix z zooms the current pane to fill the whole window; prefix z again restores it
tmux resize-pane -Z -t work:0.1   # the same zoom toggle as a command (-Z)
```
The other panes never close — they hide behind the zoom. A `Z` in the status line marks a zoomed window.
🏷️ `#pane` `#zoom`
### `prefix {` / `}` — swap panes; `prefix Space` — cycle layouts
```bash
# prefix { swaps this pane with the previous one; prefix } with the next one
# prefix Space cycles to the next preset layout (next-layout)
tmux select-layout tiled            # jump straight to a layout instead of cycling
# the five preset layouts: even-horizontal, even-vertical,
# main-horizontal, main-vertical, tiled
```
🏷️ `#pane` `#layout`
### Resizing panes — `prefix Alt-←↑↓→`, or `resize-pane`
```bash
# prefix Alt-←↑↓→ resizes by 5 cells; prefix Ctrl-←↑↓→ resizes by 1
# (both are repeatable: tap the arrow again without re-pressing the prefix)
tmux resize-pane -L 5   # shrink/grow the pane: -L left, -R right, -U up, -D down,
tmux resize-pane -D 2   # with the amount as the number at the end
```
🏷️ `#pane` `#resize`
### `prefix x` — kill a pane; `prefix !` — break it out into its own window
```bash
# prefix x asks "kill-pane? (y/n)"; prefix ! is break-pane
tmux kill-pane -t work:0.1                 # close one pane from the command line
tmux break-pane -s work:0.1                # move pane 1 of window 0 into a NEW window
# ⚠️ killing a pane ends the process running in it; breaking a pane out does not —
# the process keeps running, it just gets a window of its own
```
🏷️ `#pane` `#kill` `#danger`

---

## 📋 Copy mode & buffers — scroll back, copy, paste

### `prefix [` — enter copy mode and scroll the history
```bash
# prefix [ enters copy mode: ↑ ↓ move line by line, PgUp / PgDn page through
# the pane's scrollback history; Ctrl-s / Ctrl-r search (the default emacs
# keys — with vi mode-keys, search is / and ? instead); q quits copy mode
tmux copy-mode -t work:0.0     # enter copy mode from the command line
```
Copy mode is also how you read output that scrolled away — the mouse wheel only does this once `mouse on` is set (config section).
🏷️ `#copy-mode` `#scrollback` `#must-know`
### Copying text — the keys depend on `mode-keys` (default: emacs)
```bash
# tmux 3.4's factory default is mode-keys emacs (verified with show-options):
#   Ctrl-Space = start selection, Alt-w (or Ctrl-w) = copy and exit copy mode
# if you set:  set-window-option -g mode-keys vi
# the same job becomes vi-style:
#   Space = start selection, Enter = copy and exit copy mode
```
Either way the copied text lands on top of tmux's buffer stack — no clipboard tool needed inside tmux itself.
🏷️ `#copy-mode` `#copy`
### `prefix ]` — paste the latest buffer
```bash
# inside tmux: prefix ] pastes the most recently copied buffer at the cursor
tmux list-buffers              # show the buffer stack, newest first (buffer0, buffer1, …)
tmux paste-buffer -t work:0.0  # paste the newest buffer into a pane, from the CLI
tmux show-buffer               # print the newest buffer's contents to stdout
```
🏷️ `#buffers` `#paste` `#must-know`
### `tmux capture-pane -p` — print a pane's contents to stdout
```bash
tmux capture-pane -p -t work:0.0            # the visible screen of that pane, as text
tmux capture-pane -p -S -500 -t work:0.0    # …plus scrollback: -S -500 starts 500
                                            # lines back in the history
tmux capture-pane -p -S - -t work:0.0       # -S - means: the entire scrollback
```
`-p` is what makes it print instead of loading a buffer. This is the scripting workhorse — snapshot any pane from cron, a script, or another terminal.
🏷️ `#capture` `#scripting` `#must-know`
### `tmux save-buffer` — write a buffer to a file
```bash
tmux save-buffer ~/pane-copy.txt        # newest buffer → file (overwrites)
tmux save-buffer -a ~/pane-copy.txt     # -a appends instead of overwriting
tmux save-buffer - | wc -c              # "-" as the path writes the buffer to
                                        # stdout, so any command can read it
```
Pair it with entry 20: `capture-pane` grabs the text, `save-buffer` (or a shell redirect) puts it on disk.
🏷️ `#buffers` `#files` `#scripting`

---

## ⚙️ Configuration — ~/.tmux.conf

tmux reads `~/.tmux.conf` when the server starts. Every block below was loaded into a real server with `tmux -f` and read back with `show-options` — no dead settings.

### Change the prefix — Ctrl-b → Ctrl-a
```bash
set -g prefix C-a        # use Ctrl-a as the prefix…
unbind C-b               # …free the default Ctrl-b binding…
bind C-a send-prefix     # …and let prefix C-a send a literal Ctrl-a to the program
```
`send-prefix` matters: without it, programs that themselves use Ctrl-a (shells, editors) can never receive it.
🏷️ `#config` `#prefix`
### `set -g mouse on` — click panes, drag borders, scroll
```bash
set -g mouse on
# mouse on gives you: click a pane or window to select it, drag a pane
# border to resize, and scroll the wheel straight into copy mode
```
🏷️ `#config` `#mouse` `#must-know`
### Bigger history, 1-based indexes, auto-renumber
```bash
set -g history-limit 10000          # scrollback lines per pane (default: 2000)
set -g base-index 1                 # windows start at 1, not 0 (matches the keyboard row)
set-window-option -g pane-base-index 1   # panes start at 1 too
set -g renumber-windows on          # closing a window renumbers the rest — no gaps
```
🏷️ `#config` `#indexes`
### `prefix r` — reload the config without restarting tmux
```bash
bind r source-file ~/.tmux.conf \; display "Reloaded!"
# the \; is an escaped separator: it lets ONE key binding run TWO tmux commands
# (source-file, then display). Written as a plain ; the config parser would
# end the bind command there instead. In tmux 3.4 display shows the message
# on the status line — display-message is the same command's full name.
```
🏷️ `#config` `#reload`
### Friendlier split keys that keep your directory
```bash
bind | split-window -h -c "#{pane_current_path}"   # prefix | = side-by-side split
bind - split-window -v -c "#{pane_current_path}"   # prefix - = stacked split
# -c "#{pane_current_path}" makes the NEW pane start in the current pane's
# directory — without it, new panes/windows start in the directory the
# server was launched from, and you cd your way back every time
```
🏷️ `#config` `#split` `#keys`

---

## 🔗 Scripting & miscellany

### Drive tmux from scripts — detached sessions + `send-keys`
```bash
tmux new-session -d -s job 'make test'          # -d: start detached, run the command inside
tmux send-keys -t job 'ls -la' Enter            # type a command into a pane + press Enter
tmux send-keys -t job:0.0 'echo done' Enter     # targets can be session:window.pane
```
`send-keys` sends real keystrokes, `Enter`, `C-c` and friends included — it is how every tmux automation (and half of all "AI runs my terminal" setups) actually works.
🏷️ `#scripting` `#automation` `#must-know`
### `pipe-pane` — log a pane's output to a file
```bash
tmux pipe-pane -t job -o 'cat >>~/job.log'   # start logging pane "job" (append)
tmux pipe-pane -t job                        # run again with no command = stop logging
# -o means "only open the pipe if none is open" — scripts can run the start
# line repeatedly without accidentally toggling the logging off
```
🏷️ `#scripting` `#logging`
### `prefix ?` — list every key binding
```bash
# inside tmux: prefix ? opens the full binding list in a pager (q to leave)
tmux list-keys                 # the same table from the command line — all tables
tmux list-keys -T prefix       # only the prefix table: the definitive answer to
                               # "what does prefix + <key> actually do?"
```
When any cheat sheet (this one included) disagrees with your machine, `list-keys` wins — it prints the bindings your server is really using, custom config included.
🏷️ `#help` `#keys` `#reference`
### `choose-tree` — and the last resort, `kill-server`
```bash
# inside tmux: prefix s = session tree, prefix w = tree of sessions + windows
tmux choose-tree -Zs           # the command behind prefix s — it renders inside
                               # an attached client, so use it from within tmux;
                               # from a plain shell, tmux ls / list-windows list instead
tmux kill-server               # ⚠️ LAST RESORT: stops the tmux server itself —
                               # EVERY session, window and process dies at once.
                               # Reach for kill-session (entry 5) instead, unless
                               # the server is truly wedged.
```
🏷️ `#danger` `#kill` `#reference`

---

## Contributing

Found a wrong command, an outdated key, or a bad translation? Pull requests are welcome — keep entries to the format above (one-liner / bash block / tags) and **only real, verified commands; when in doubt, leave it out**.

## License

MIT © 2026 Guangyi Zhao. See [LICENSE](LICENSE).
