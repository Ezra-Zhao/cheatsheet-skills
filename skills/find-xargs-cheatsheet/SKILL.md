---
name: find-xargs-cheatsheet
description: 'Use when the user needs find or xargs commands: finding files by name, size, date, type or permissions, running commands on matches with -exec and -execdir, deleting safely, -print0 with xargs -0 for filenames with spaces, and parallel runs with xargs -P.'
---

# find + xargs Cheatsheet — Commands That Actually Work

One page. Thirty entries: finding files by name, type, size, time and permissions; combining tests without falling into the `-o`/`-print` trap; running commands with `-exec`, `-execdir` and `-printf`; and feeding the results to `xargs` — safely, with `-print0`/`-0`, in parallel with `-P`, one batch at a time with `-n` and `-I`. No made-up flags — every entry was **run for real** against a test tree with GNU findutils 4.9.0, and the semantics checked against the GNU Findutils manual (`find`, `xargs`).

> 🌍 Read this project in your language: [中文](README.md) · [Español](README.es.md) · [Português](README.pt.md)

Docs: https://www.gnu.org/software/findutils/manual/

---

## 🔍 Basics — where to look, and by name

### `find . -name "*.log"` — find by name pattern
```bash
find . -name "*.log"        # every .log file under the current directory
find /var/log -name "*.gz"  # ...or start from any directory you name
```
The pattern matches the **base name** only (no directories), it is a shell-style glob (not a regex), and it is case-sensitive. The starting path defaults to `.` and the default action is `-print`.
🏷️ `#basics` `#name` `#must-know`
### `find . -iname` — the same search, case-insensitive
```bash
find . -iname "readme*"     # matches ReadMe.TXT, README.md, readme.txt alike
find . -name "readme*"      # matches ONLY the all-lowercase one — feel the difference
```
Most name/path tests come in pairs: the plain one is case-sensitive, the `i`-version (`-iname`, `-ipath`, `-iregex`) is not.
🏷️ `#basics` `#name`
### `find . -type` — files, directories, symlinks
```bash
find . -type f    # regular files only
find . -type d    # directories only
find . -type l    # symlinks only (the links themselves — find does not follow them by default)
```
Type letters: `f` file, `d` directory, `l` symlink, `s` socket, `p` named pipe, `b`/`c` block/char device. Half of all real searches are `-type f` plus something else.
🏷️ `#basics` `#type` `#must-know`
### `find . -path` — match the whole path, not just the name
```bash
find . -path "*/src/*.js"   # .js files with a src directory anywhere above them
```
`-path` tests the pattern against the **entire path** (`./src/main.js`), and — unlike shell globbing — its `*` happily matches `/` too. That's what makes `*/src/*` work without any special syntax.
🏷️ `#basics` `#path`
### `-maxdepth` / `-mindepth` — control how deep find digs
```bash
find . -maxdepth 1 -type f     # only files directly in . — no subdirectories
find . -mindepth 2 -name "deep.txt"   # skip the top two levels, then look
```
Depth counts from the starting point: `.` itself is depth 0, `./src` is depth 1. These are *global options* — put them before the tests, or GNU find warns and applies them globally anyway.
🏷️ `#basics` `#depth`

---

## 🎯 Filters — size, time, owner of the mess

### `-size` — find the disk hogs (mind the rounding)
```bash
find . -type f -size +1M    # bigger than 1 MiB — the disk-space hunt
find . -name "small.txt" -size -10k   # under 10 KiB
```
Units: `c` bytes, `k` KiB, `M` MiB, `G` GiB; `+` means more than, `-` means less than. ⚠️ Sizes are **rounded up** to whole units before comparing — so `-size -1M` matches only *empty* files (anything non-empty rounds up to 1). For byte-exact thinking use `c`: `-size -1048576c`.
🏷️ `#filters` `#size` `#disk`
### `-mtime` / `-mmin` — by modification time
```bash
find . -type f -mtime -7    # modified within the last 7 days
find . -type f -mmin -60    # modified within the last 60 minutes
```
`-mtime n` counts whole 24-hour periods (any fraction is dropped): `-mtime -7` = 0–6 periods ago, `-mtime 7` = the 7th day back. `-mmin` is the same idea in minutes; `-atime`/`-ctime` test access/inode-change instead of modification.
🏷️ `#filters` `#time` `#must-know`
### `-newer` — newer than a reference file
```bash
find . -type f -newer marker.txt   # everything modified after marker.txt was
```
The "what changed since the release marker / since the backup" search. The reference file itself is *not* included (it is not newer than itself). Variants: `-anewer` (access), `-cnewer` (inode change).
🏷️ `#filters` `#time`
### `-empty` — empty files and empty directories
```bash
find . -empty    # zero-byte files AND directories with nothing in them
```
The cleanup pre-scan — and the natural partner of `-delete` (below): look first, delete second.
🏷️ `#filters` `#cleanup`
### `-perm` — by permission bits, three ways
```bash
find . -type f -perm 755        # exactly these bits, no more, no less
find . -type f -perm -u=x       # the user-execute bit must be SET (other bits: don't care)
find . -type f -perm /g=w,o=w   # group-write OR other-write — ANY listed bit set matches
```
No prefix = exact match. `-` prefix = **all** listed bits must be set. `/` prefix = **any** listed bit set is enough. Symbolic (`u=x`) and octal (`755`) modes both work.
🏷️ `#filters` `#permissions` `#security`
### `-regex` — when a glob is not enough
```bash
find . -regex ".*\.\(log\|txt\)"   # paths ending in .log or .txt
```
The pattern must match the **whole path** (that's why it starts with `.*`), and the default dialect is Emacs regex — `\(...\)` for groups, `\|` for alternation. `-regextype posix-extended` switches to the dialect where `(log|txt)` works bare; `-iregex` is the case-insensitive version.
🏷️ `#filters` `#regex`

---

## 🧩 Combining tests — AND, OR, NOT, and the -print trap

### `\( ... -o ... \)` — parentheses make OR behave
```bash
find . -type f \( -name "*.log" -o -name "*.js" \)   # .log OR .js, and a regular file either way
find . -type f ! -name "*.log"                        # NOT: every file except the logs (! is -not)
```
Tests side by side are AND. `-o` is OR, but it binds **looser** than AND — without `\( \)` the `-type f` above would apply only to the left branch. (In the shell, the parentheses need the backslashes.)
⚠️ The classic trap: in `find . -name "*.log" -o -name "*.js" -print`, the `-print` belongs only to the *right* branch — you silently get just the `.js` files. Rule: if you add an action to an expression containing `-o`, wrap the tests in `\( \)` first.
🏷️ `#logic` `#must-know` `#gotcha`

---

## ⚙️ Actions — do something with the matches

### `-exec ... \;` — run a command once per file
```bash
find . -name "*.log" -exec wc -l {} \;   # {} is replaced by the file's path, one run per file
```
`{}` is where the path goes; `\;` ends the command (the backslash stops the shell eating the `;`). One process per file — simple and predictable, slow on thousands of files.
🏷️ `#actions` `#exec` `#must-know`
### `-exec ... {} +` — batch the files into few runs
```bash
find . -name "*.log" -exec wc -l {} +   # wc runs ONCE with both files (note the "total" line)
```
The `+` form appends as many paths as fit on one command line — the find-native version of what xargs does, and dramatically faster than `\;`. `{}` must be the last thing before the `+`, and only one `{}` is allowed.
🏷️ `#actions` `#exec` `#performance`
### `-execdir` — run from inside each file's own directory
```bash
find . -name "deep.txt" -execdir pwd \;   # prints .../deep/a/b/c — the directory holding the file
```
`-execdir` changes into the directory containing each match first, and `{}` becomes `./deep.txt` there. Reach for it when the command expects local names (per-directory builds, `tar` of siblings) — and as the safer default, since it never hands a command a path starting deep in a tree it didn't expect.
🏷️ `#actions` `#exec`
### `-ok` — like -exec, but asks first
```bash
find . -name "*.log" -ok echo FOUND {} \;
# < echo ... ./app.log > ?   ← type y to run it for this file, anything else to skip
```
The rehearsal mode for destructive actions: swap `-ok` in while you tune the search, watch what *would* run, then switch to `-exec` (or `-delete`) when the list looks right.
🏷️ `#actions` `#safety`
### `-printf` — print exactly the fields you want
```bash
find . -name "notes.txt" -printf "%s %p\n"   # size in bytes, then the path: 36 ./notes.txt
```
Format directives: `%p` path, `%f` base name, `%s` size in bytes, `%TY-%Tm-%Td` modification date, `%u` owner, `%%` a literal %. When the output feeds a script or a report, `-printf` beats parsing `-ls`.
🏷️ `#actions` `#printf` `#scripting`
### `-ls` — an ls-style listing of the matches
```bash
find . -name "app.log" -ls   # inode, blocks, mode, owner, size, date, path — ls -dils in one flag
```
Good for the "show me what it's about to touch" pass before an `-exec rm` or a `-delete`.
🏷️ `#actions` `#ls`
### `-delete` — delete the matches (look first!)
```bash
find . -name "*.tmp" -delete   # deletes matching files — here inside a scratch copy, rehearse first
```
`-delete` implies `-depth` (contents are processed before the directories holding them) and refuses to remove non-empty directories. There is no undo and no trash can: run the same search with `-print` (or `-ls`) first, every time.
🏷️ `#actions` `#delete` `#danger`

---

## 🚀 xargs — feed the list to a command

### The basic pipe — find | xargs
```bash
find . -name "*.log" | xargs grep -l "ERROR"   # which log files contain an error?
```
`xargs` reads items from stdin and appends them to the command line. ⚠️ Plain pipes split on **any whitespace** and process quotes — a file named `file with spaces.txt` arrives as three broken arguments. That's the bug the next entry exists to fix.
🏷️ `#xargs` `#pipe` `#must-know`
### `-print0` | `xargs -0` — the pair that survives any filename
```bash
find . -name "*.txt" -print0 | xargs -0 grep -l "TODO"
# finds the TODO in notes.txt AND in "file with spaces.txt" — names arrive intact
```
Filenames can contain spaces, quotes and even newlines — the only byte they can never contain is NUL, so NUL becomes the separator: find prints `name\0`, xargs `-0` reads `name\0`. Use this pair whenever the tree isn't yours. (One side effect to know: a command like `grep` follows symlinks you hand it as arguments, so a link to a matching file gets listed too.)
🏷️ `#xargs` `#safety` `#must-know`
### `xargs -n` — at most N arguments per run
```bash
printf '1\n2\n3\n4\n5\n' | xargs -n 2 echo   # runs echo three times: "1 2", "3 4", "5"
```
Batching control: keep each invocation small when the command is expensive per-argument or has its own argument limits. (`-L n` is the same idea counted in input *lines*.)
🏷️ `#xargs` `#batching`
### `xargs -I{}` — put each item exactly where you want it
```bash
printf 'a.txt\nb.txt\n' | xargs -I{} cp {} {}.bak   # a.txt → a.txt.bak, b.txt → b.txt.bak
```
`-I` replaces the placeholder (here `{}`) **wherever it appears** in the command — even inside a word like `{}.bak`. It implies one input line per run, so it's the precise-but-slower tool: templates and per-file output names are its home turf.
🏷️ `#xargs` `#templates` `#must-know`
### `xargs -P` — run the commands in parallel
```bash
printf 'a\nb\nc\nd\n' | xargs -P 4 -I{} sh -c 'echo JOB-{}'   # four jobs at once (order not guaranteed)
```
`-P n` keeps up to *n* processes running at once — the one-flag speedup for CPU-bound batches (image thumbs, test shards, transcodes). Output from parallel jobs interleaves in whatever order they finish; sort afterwards if order matters. `-P 0` means "as many as possible".
🏷️ `#xargs` `#parallel` `#performance`
### `xargs -t` — show each command before running it
```bash
printf 'hello\n' | xargs -t echo   # stderr shows "echo hello", then stdout gets "hello"
```
The verbose flag: xargs prints every command it builds to **stderr** before executing. First thing to add when a pipeline "does nothing" — usually the command it built isn't the one you pictured.
🏷️ `#xargs` `#debug`
### `xargs -p` — ask before each command runs
```bash
printf 'zz\n' | xargs -p echo PONG   # asks "echo PONG zz?..." on the terminal; y runs it, n skips
```
Interactive mode — `-t` plus a yes/no prompt per command, read from the terminal (not from the piped stdin, which is busy carrying the items). The rehearsal tool for commands you'd rather not fire blind.
🏷️ `#xargs` `#safety`
### `xargs -r` — do nothing when the input is empty
```bash
printf '' | xargs -r echo RAN   # prints NOTHING — the command never runs
printf '' | xargs echo RAN      # prints "RAN" — without -r, xargs runs the command once anyway
```
GNU xargs runs the command **once even with zero items** unless you pass `-r` (`--no-run-if-empty`). In scripts driven by `find`, that one phantom run is a classic bug — make `-r` a habit. (This sheet is GNU findutils; BSD/macOS xargs differs in places — check the local man page before porting a script.)
🏷️ `#xargs` `#scripting` `#gotcha`
### `xargs -d` — choose the separator yourself
```bash
printf 'file with spaces.txt\nnotes.txt\n' | xargs -d '\n' -n1 echo
# one name per line, spaces intact — newline is the ONLY separator now
```
`-d '\n'` keeps names with spaces safe *without* `-print0` on the producing side — but a name containing a newline still breaks it, and quote processing is switched off. (`-d` is a GNU extension — BSD xargs doesn't have it.) For hostile trees, `-print0`/`-0` stays the gold standard; `-d` is the quick fix for merely untidy ones.
🏷️ `#xargs` `#delimiter`
### `xargs -a` — read the items from a file, not stdin
```bash
xargs -a args.txt echo   # args.txt holds "alpha beta" and "gamma" → runs: echo alpha beta gamma
```
Handy when the item list already lives in a file (a manifest, a build artifact) — no `cat file |` needed, and stdin stays free for the command itself.
🏷️ `#xargs` `#files`
### `xargs -E` — stop reading at a marker line
```bash
printf 'one\ntwo\nEND\nthree\n' | xargs -E END echo   # prints "one two" — "three" is never read
```
A logical end-of-file string: the first input line that *is* the marker ends the list (the marker itself is not included). For generated lists with a sentinel — config sections, heredoc-built manifests. (Ignored when `-0` or `-d` is in play.)
🏷️ `#xargs` `#eof`

---

## Contributing

Found a wrong command, an outdated flag, or a bad translation? Pull requests are welcome — keep entries to the format above (one-liner / bash block / tags) and **only real, verified commands; when in doubt, leave it out**.

## License

MIT © 2026 Guangyi Zhao. See [LICENSE](LICENSE).
