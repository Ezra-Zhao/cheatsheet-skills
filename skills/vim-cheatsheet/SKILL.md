---
name: vim-cheatsheet
description: 'Use when the user needs Vim commands: modes, movement, editing operators, search and replace, visual mode, macros, registers, marks, buffers, windows and tabs, and saving or quitting without losing work.'
---

# Vim Cheatsheet — Commands That Actually Work

One page. Thirty entries: quitting and saving without fear, moving fast, editing with operators and text objects, search & replace, visual mode, and macros. Each entry tells you **what it does**, **keys you can copy-paste**, and **tags**. No made-up commands — almost every entry was run headless in this machine's Vim 9.1 (vim-tiny) and the resulting file checked; the few entries a tiny build cannot run (system clipboard, `:nohlsearch`, persistent undo, the sudo save) were verified against Vim's own feature flags and documentation behaviour instead — see the notes on those entries.

> 🌍 Read this project in your language: [中文](README.md) · [Español](README.es.md) · [Português](README.pt.md)

Docs: https://www.vim.org/docs.php

---

## 🚪 Quitting & saving

### `:w` / `:q` / `:wq` and `ZZ` — write, quit, or both
```vim
:w          " write (save) the file, stay in Vim
:q          " quit — Vim refuses if there are unsaved changes
:wq         " write AND quit
ZZ          " normal-mode twin of :wq — but like :x, it only writes if modified
```
🏷️ `#quit` `#save` `#basics` `#must-know`
### `:q!` and `ZQ` — quit and throw the changes away
```vim
:q!         " quit WITHOUT saving — unsaved changes are discarded
ZQ          " normal-mode twin of :q!
```
⚠️ There is no undo after `:q!` / `ZQ` — the edits never reached the disk, so they are gone. Use it when the buffer is a mess and the file on disk is the version you trust.
🏷️ `#quit` `#rescue` `#must-know`
### `:x` vs `:wq` — `:x` doesn't touch an unchanged file
```vim
:x          " write ONLY if the buffer was modified, then quit
:wq         " always writes, even if nothing changed
```
The difference is real: on an unmodified file `:x` leaves the file's modification time untouched, while `:wq` rewrites it and bumps the mtime (verified by test: the `:x` file kept its old timestamp, the `:wq` file did not). Backups, build tools and `rsync` all key off mtime — prefer `:x`.
🏷️ `#quit` `#save`
### `:w !sudo tee %` — save a file you opened without sudo
```vim
:w !sudo tee %
" Vim pipes the whole buffer to `sudo tee`, and tee (running as root)
" writes it back over % — the file you forgot to open with sudo.
" On a machine without sudo, any privileged writer works the same way:
" it is the `:w !cmd` plumbing that matters.
```
🏷️ `#save` `#sudo` `#rescue`
### Open at a line or a match — `vim +42 file`, `vim +/pattern file`
```bash
vim +42 notes.txt          # open with the cursor on line 42
vim +/TODO notes.txt       # open on the first line matching TODO
vim + notes.txt            # open on the last line
```
🏷️ `#open` `#basics`

---

## 🧭 Moving

### `h j k l` and `w b e` — the keys your fingers live on
```vim
h j k l     " left / down / up / right
w           " next word start      b  previous word start
e           " next word end
W B E       " same, but WORD = anything between spaces (punctuation counts as part of the word)
```
🏷️ `#move` `#basics` `#must-know`
### `0 ^ $`, `gg G`, `:{n}` and `{n}G` — line anchors and jumps
```vim
0           " column 1            ^  first non-blank character
$           " end of line
gg          " first line          G  last line
:42         " go to line 42       42G  the same, from normal mode
```
🏷️ `#move` `#basics`
### `f F t T` with `;` and `,` — find a character on this line
```vim
f,          " jump ONTO the next comma     F,  onto the previous comma
t,          " jump to JUST BEFORE the next comma   T,  just after the previous one
;           " repeat the last f/F/t/T        ,  repeat it in the opposite direction
```
🏷️ `#move` `#must-know`
### `%` and `{ }` — matching pairs and paragraphs
```vim
%           " jump to the matching ( ) { } [ ] — works from either side
}           " next paragraph (blank-line boundary)    {  previous paragraph
```
🏷️ `#move`
### `Ctrl-d/u/f/b` and `H M L` — scrolling and screen anchors
```vim
Ctrl-d      " half a page down     Ctrl-u  half a page up
Ctrl-f      " a full page forward  Ctrl-b  a full page back
H           " top line of the screen   M  middle   L  bottom
```
🏷️ `#move` `#scroll`
### `gj` / `gk` — move by display line when lines wrap
```vim
gj          " one DISPLAY line down — inside a wrapped long line, not the next buffer line
gk          " one display line up (plain j/k jump whole buffer lines instead)
```
🏷️ `#move` `#wrap`

---

## ✏️ Editing

### `i a I A o O` — six doors into insert mode
```vim
i           " insert before the cursor     a  insert after the cursor (append)
I           " insert at the first non-blank  A  insert at the end of the line
o           " open a new line BELOW and insert   O  open a new line ABOVE
```
🏷️ `#edit` `#insert` `#basics` `#must-know`
### `x`, `dd`, `yy`, `p`, `P` with counts — delete, yank, paste
```vim
x           " delete the character under the cursor
dd          " delete the whole line        yy  yank (copy) the whole line
p           " paste after / below          P   paste before / above
3dd         " delete 3 lines               2yy  yank 2 lines — counts work everywhere
```
🏷️ `#edit` `#basics` `#must-know`
### `u`, `Ctrl-r` and `.` — undo, redo, repeat
```vim
u           " undo the last change         Ctrl-r  redo what undo took back
.           " repeat the last change — after dw, . deletes the next word the same way
```
🏷️ `#edit` `#undo` `#must-know`
### Operators `d` / `c` / `y` + a motion — Vim's grammar
```vim
dw          " delete to the next word start
d$          " delete to the end of the line
y}          " yank to the end of the paragraph
ciw         " change inner word (see the text-objects entry — c is d plus insert mode)
```
Learn `operator + motion` once and hundreds of combinations come free — the same motions from the movement section all plug in here.
🏷️ `#edit` `#operators` `#must-know`
### Text objects — `ciw`, `ci"`, `dap`, `di(`
```vim
ciw         " change inner word — the whole word, wherever the cursor sits in it
ci"         " change inside the quotes — replaces the quoted text, keeps the quotes
di(         " delete inside the parentheses — leaves func() standing
dap         " delete a paragraph (the paragraph AND its trailing blank line)
```
`i` = inner (contents only), `a` = a/around (contents plus the quotes, brackets or blank line).
🏷️ `#edit` `#text-objects`
### `r`, `~`, `>>` `<<` and `=` — small fixes
```vim
rx          " replace the character under the cursor with x (no insert mode)
~           " swap the case of the character under the cursor
>>          " indent this line     <<  un-indent it
=}          " auto-indent to the end of the paragraph (== does one line)
```
🏷️ `#edit` `#format`
### `J` and `:m` — join lines, move lines
```vim
J           " join the next line onto this one (with a space between)
:m +1       " move the current line one line DOWN
:m -2       " move the current line one line UP — :move puts the line AFTER the
            " address you name, so the count is off by one going up
            " (:m -3 = two lines up, :m -1 = no-op; :m 0 = top of file, :m $ = bottom)
```
🏷️ `#edit` `#lines`

---

## 🔍 Search & replace

### `/` `?`, `n N`, and `* #` — searching
```vim
/foo        " search forward for foo       ?foo  search backward
n           " next match                   N     previous match (opposite direction)
*           " search forward for the word under the cursor
#           " search backward for the word under the cursor
```
🏷️ `#search` `#basics` `#must-know`
### `:s` — substitute on the current line, `g` and `c` flags
```vim
:s/foo/bar/     " replace the FIRST foo on this line
:s/foo/bar/g    " g = global: every foo on the line
:s/foo/bar/gc   " c = confirm: Vim asks y/n for each match before touching it
```
🏷️ `#replace` `#must-know`
### `:%s` and `:12,20s` — whole file and ranges
```vim
:%s/foo/bar/g       " every line in the file: replace all foo with bar
:12,20s/foo/bar/g   " only lines 12 to 20
```
⚠️ `:%s` reaches the **whole file** — one wrong pattern rewrites hundreds of lines before you notice. When in doubt, add the `c` flag (`:%s/foo/bar/gc`) and confirm match by match; `u` undoes the whole substitution if it went wrong.
🏷️ `#replace`
### Search settings — `\c`, `ignorecase`/`smartcase`, `hlsearch`/`incsearch`, `:noh`
```vim
/\cHello        " \c in the pattern: ignore case for THIS search (\C forces case)
:set ignorecase smartcase
                " ignorecase: searches are case-insensitive…
                " …unless smartcase sees an uppercase letter in the pattern
:set hlsearch incsearch
                " hlsearch: highlight all matches   incsearch: jump while you type
:noh            " clear the match highlighting until the next search (:nohlsearch in full)
```
🏷️ `#search` `#settings`
### `:g/pattern/d` and `:v` — the global command
```vim
:g/TODO/d       " delete EVERY line that matches TODO, in one command
:v/keep/d       " :v is :g inverted — delete every line that does NOT match keep
```
`:g` runs any Ex command on matching lines (`:g/pattern/p` prints them, `:g/pattern/t$` copies them to the end); delete is just the most-used case.
🏷️ `#search` `#global` `#power`

---

## 👁 Visual mode

### `v`, `V`, `Ctrl-v` — the three visual modes
```vim
v           " character-wise selection — then y yanks it, d deletes it, ~ flips case…
V           " LINE-wise selection — whole lines, however far you extend
Ctrl-v      " BLOCK-wise selection — a rectangle across lines (next two entries)
```
🏷️ `#visual` `#basics` `#must-know`
### Block insert and append — `Ctrl-v` then `I`, and `$ A`
```vim
Ctrl-v  j j  I- <Esc>
            " select a block over 3 lines, I inserts "- " at the block's
            " left edge on EVERY line when you press Esc
Ctrl-v  j j  $ A;<Esc>
            " $ extends the block to each line's end, A appends ";" everywhere
```
🏷️ `#visual` `#block` `#power`
### `gv` and `o` — reselect, and swap ends
```vim
gv          " re-select the last visual selection (after Esc, a command, anything)
o           " while selecting: jump the cursor to the OTHER end of the selection —
            " fix the start of the selection without redoing the whole thing
```
🏷️ `#visual`

---

## 🎙 Macros & more

### Macros — `q{a-z}` records, `@{a-z}` plays, counts multiply
```vim
qa          " start recording into register a (any of a–z)
…do the edit once…
q           " stop recording
@a          " play it back once        @@  play the last-played macro again
10@a        " play it 10 times — the count is how macros pay off
```
A complete, tested example — put `- ` at the start of every line: park the cursor on line 1, then `qa`, `I- `, `Esc`, `j`, `q` (recorded: insert `- `, drop a line). Now `2@a` does lines 2–3, `9@a` does the next nine lines the same way. Record once, on real text, with the `j` *inside* the macro so playback walks down the file by itself.
🏷️ `#macros` `#power` `#must-know`
### Registers — `:registers`, `"ayy`, `"+y`
```vim
:registers      " list every register and what it holds
"ayy            " yank this line into register a (named registers survive later yy/dd)
"ap             " paste from register a
"+y             " yank to the SYSTEM clipboard — needs a Vim built with +clipboard:
                " check yours with `vim --version | grep clipboard` (+clipboard = yes)
```
🏷️ `#registers` `#clipboard`
### `:!cmd` and `:r !cmd` — shell out, and read results in
```vim
:!ls -la        " run a shell command (output is shown, the file is untouched)
:r !date        " READ the command's output into the buffer, below the cursor —
                " today's date lands in the file; :r !hostname works the same way
```
🏷️ `#shell` `#power`
### A survival `~/.vimrc` — four lines that pay daily
```vim
set number relativenumber   " line numbers: absolute here, relative around it (jumps get easy)
set expandtab shiftwidth=2  " Tab inserts spaces, one indent level = 2 of them
set ignorecase smartcase    " case-insensitive search, unless you type a capital
set undofile                " keep undo history in a file — undo survives closing Vim
                            " (needs a Vim built with +persistent_undo; most full builds have it)
```
🏷️ `#vimrc` `#settings` `#setup`

---

## Contributing

Found a wrong command, an outdated flag, or a bad translation? Pull requests are welcome — keep entries to the format above (one-liner / code block / tags) and **only real, verified commands; when in doubt, leave it out**.

## License

MIT © 2026 Guangyi Zhao. See [LICENSE](LICENSE).
