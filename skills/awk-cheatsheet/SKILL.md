---
name: awk-cheatsheet
description: 'Use when the user needs awk commands: printing fields and whole lines, NR/FNR line counters, BEGIN/END blocks, regex and range patterns, FS/OFS separators, sub/gsub/split/match string work, summing and averaging columns, order-preserving dedupe, group-by totals, word frequency, and the NR==FNR two-file join.'
---

# awk Cheatsheet — Commands That Actually Work

One page. Thirty entries: the pattern–action shape every awk program is built from; fields, records and the two line counters; choosing lines with regexes, ranges and comparisons; the built-in variables and string functions that do the real work; and the one-liner recipes — sum, average, dedupe, group-by, the two-file join — that people actually keep in their shell history. No made-up syntax — every entry was **run for real** against fixture files with mawk 1.3.4 (the awk this machine ships), and the semantics checked against the GNU Awk User's Guide. Where GNU awk (gawk) and mawk/BusyBox differ, the sheet says so.

> 🌍 Read this project in your language: [中文](README.md) · [Español](README.es.md) · [Português](README.pt.md)

Docs: https://www.gnu.org/software/gawk/manual/

---

## 🧱 Basics — records, fields, and the pattern–action shape

### `awk '{print $0}'` — the whole line, untouched
```bash
awk '{print}' scores.txt        # print with nothing after it prints $0
awk '{print $0}' scores.txt     # the same command, spelled out — $0 is the whole record
```
An awk program is a list of `pattern { action }` pairs, tested once per input line (a *record*). Before the action runs, the record is split into fields on runs of whitespace. `$0` is the record exactly as read — splitting never changes it.
🏷️ `#basics` `#print` `#must-know`
### Fields — `$1`, `$NF`, and `NF`
```bash
awk '{print $1, $NF}' scores.txt   # $1 is the first field, $NF the last one
awk '{print NF}' words.txt         # NF: how many fields this line split into (0 for an empty line)
```
`$2`, `$3`, … go as far as the line does; `NF` holds the field count, so `$(NF-1)` is the second-to-last field. Watch the commas in `print $1, $NF`: they become a single space (the value of `OFS`) — the line's original spacing is *not* preserved.
🏷️ `#basics` `#fields` `#must-know`
### `NR` and `FNR` — two line counters
```bash
awk '{print NR": "$0}' part1.csv part2.csv     # NR counts across ALL files: 1 to 6
awk '{print FNR": "$0}' part1.csv part2.csv    # FNR restarts at 1 for each new file
```
`NR` is the total number of records read so far; `FNR` is the record number within the file currently being read. `FILENAME` holds that file's name. Everything later in this sheet that touches more than one file — headers, joins — is built on the difference between these two.
🏷️ `#basics` `#counters`
### `BEGIN` and `END` — setup before, summary after
```bash
awk 'BEGIN {print "name subject score"} {n++} END {print n, "rows read"}' scores.txt
```
`BEGIN` runs once, before the first record is read — the place for headers and for setting `FS`. `END` runs once, after the last record — the place for totals and averages. In `END`, `NR` still holds the grand total of records read.
🏷️ `#basics` `#begin-end` `#must-know`
### A pattern alone prints; an action alone runs everywhere
```bash
awk '/ERROR/' app.log          # pattern, no action: matching lines are printed (print $0 is the default action)
awk '{print $1}' app.log       # action, no pattern: runs on every line
```
The two defaults that make awk one-liners so short: a missing action means `print $0`, and a missing pattern means "true". Half the awk in the wild is just one side of the pair.
🏷️ `#basics` `#patterns`
### Your own variables — and `-v` to hand values in
```bash
awk -v min=85 '$3 >= min {print $1, $3}' scores.txt   # -v sets the variable before the program starts
awk '{n++} END {print n+0}' empty.txt                 # empty input: n was never touched — n+0 forces a numeric 0 instead of ""
```
Variables need no declaration and hold a number, a string, or "uninitialized" — which reads as `0` in math and `""` in string context. The `n+0` trick pins the numeric reading when a count must print as `0`, not as a blank. `-v` assignments happen before `BEGIN` runs, so `BEGIN` can use them too.
🏷️ `#basics` `#variables`

---

## 🎯 Patterns — choose which lines to touch

### `/regex/` — match anywhere in the line
```bash
awk '/ERROR|WARN/' app.log     # the pattern is tested against the whole line ($0)
```
A bare `/…/` pattern is a *match* test, not an equality test: it succeeds if the regex matches anywhere in the record. `^` and `$` anchor to the start and end of the whole line, not of a field.
🏷️ `#patterns` `#regex` `#must-know`
### `/start/,/end/` — range patterns
```bash
awk '/START/,/END/' app.log    # from the line matching START through the line matching END, both included
```
A range pattern switches on when a line matches the first pattern and stays on until a line matches the second — that closing line is included too. If the start pattern matches again further down, a fresh range begins. And if one line matches both, the range is just that line.
🏷️ `#patterns` `#range`
### Comparisons — numbers compare as numbers, strings as strings
```bash
awk '$3 >= 85 {print $1, $3}' scores.txt        # field vs number: numeric comparison
awk '$2 == "math" {print $1, $3}' scores.txt    # field vs "quoted": string comparison
```
⚠️ The constant you compare against picks the comparison type. A field that looks like a number, compared against an *unquoted* number, compares numerically — `"010" == 10` is true. Against a *quoted* string it compares as text — `"010" == "10"` is false. Choose the quotes on purpose; this is the single most surprising thing in awk.
🏷️ `#patterns` `#comparison` `#gotcha`
### `~` and `!~` — match one field, not the whole line
```bash
awk -F: '$1 ~ /^(root|daemon)$/ {print $1}' passwd.txt   # ~ : this field matches the regex
awk '$7 !~ /\.png$/ {print $7}' access.log               # !~ : this field does NOT match
```
`field ~ /regex/` asks the match question about one field instead of `$0`. Anchors now bind to the field's edges, which is what makes `$1 ~ /^(root|daemon)$/` an exact-name test rather than a substring test.
🏷️ `#patterns` `#regex` `#must-know`
### `&&`, `||`, `!` — combine tests
```bash
awk '$9 >= 400 && $9 < 600 {print $9, $7}' access.log   # both sides: the 4xx and 5xx requests, with their paths
awk '!($3 >= 60) {print $1, $2, $3}' scores.txt         # ! negates — here, the one failing score
```
Patterns are full boolean expressions: `&&` (and), `||` (or), `!` (not), parentheses for grouping. Most real-world filters are one of these wrapped around two comparisons.
🏷️ `#patterns` `#logic`
### `FNR > 1` — skip every file's header
```bash
awk -F, 'FNR > 1 {n++} END {print n}' part1.csv part2.csv   # 4 — FNR restarts, so each header is "line 1" and gets skipped
awk -F, 'NR > 1 {n++} END {print n}' part1.csv part2.csv    # 5 — NR skips only the very first line of the whole run
```
⚠️ The `NR > 1` version is the classic multi-file bug: the second file's header sails through as if it were data — counted here, and quietly converted to `0` if you sum its column. `FNR` exists precisely for this.
🏷️ `#patterns` `#files` `#gotcha`

---

## 🧰 Built-in variables & functions

### `-F` and `FS` — choose the separator
```bash
awk -F: '{print $1, $7}' passwd.txt                    # -F takes a regular expression; ":" here is a plain char
awk 'BEGIN {FS = ","} {print $1, $3}' people.csv       # or set FS in BEGIN, before the first record is split
```
The separator is the variable `FS`: a single character, or a regular expression — `-F'[,:]'` splits on commas *and* colons. One value is special: `FS = " "` (a single space, the default) means "any run of blanks and tabs", and leading/trailing whitespace is ignored — that's why `$1` of an indented line is its first word, not an empty string.
🏷️ `#variables` `#fs` `#must-know`
### Assigning a field rebuilds `$0` — with `OFS`
```bash
awk '{$1 = $1; print}' messy.txt                          # even $1 = $1 rebuilds the record: whitespace runs collapse to OFS
awk 'BEGIN {OFS = "-"} {$1 = $1; print}' messy.txt        # the rebuild joins the fields with OFS — here, dashes
```
Reading fields never touches `$0`. *Assigning* to any field (or to `NF`) rebuilds `$0` from `$1`…`$NF`, joined by `OFS` (a space by default). The `$1 = $1` no-op is the standard whitespace normalizer — and the reason a "harmless" field edit can reformat an entire file.
🏷️ `#variables` `#ofs` `#gotcha`
### `length()` — how long is this string
```bash
awk '{print length($0), $0}' words.txt     # characters in the string (an empty line scores 0)
awk 'length($0) > 10 {print}' words.txt    # the same call used as the pattern: only long lines pass
```
Called with no argument, `length()` measures `$0`. ⚠️ What it counts depends on the implementation: the GNU Awk manual defines the count in *characters*, but this machine's mawk counts *bytes* — the four-character string `你好世界` measures 12 here, not 4 (verified). On ASCII text the two never differ.
🏷️ `#functions` `#strings`
### `substr()` — cut a piece out of a string
```bash
awk '{print substr($4, 2, 11)}' access.log   # substr(s, start, len) — positions count from 1: the date out of "[08/Nov/2026:..."
awk '{print substr($1, 1, 3)}' scores.txt    # the first three characters of field 1
```
Positions count from **1**, not 0. Leave the length off to take everything to the end of the string; asking for more than remains just stops at the end instead of erroring.
🏷️ `#functions` `#strings`
### `split()` — chop a string into an array
```bash
awk '{n = split($4, d, "[/:]"); print d[2], n}' access.log   # split returns the piece count; d[1]="[08", d[2]="Nov"
```
`split(string, array, separator)` fills `array[1]`, `array[2]`, … and returns how many pieces it made. The separator is a regex; leave it off to split on `FS`; use `""` to cut the string into single characters.
🏷️ `#functions` `#arrays` `#strings`
### `sub()` and `gsub()` — replace by regex
```bash
awk '{sub(/[ \t]+$/, ""); print}' messy.txt                # sub: FIRST match only — here it trims trailing whitespace
awk '{n = gsub(/ /, "_"); print n, $0}' access.log         # gsub: EVERY match — and it returns how many it replaced
awk '{gsub(/[0-9]+/, "<&>"); print}' access.log            # in the replacement, & means "the text that just matched"
```
Both edit their target in place (`$0` by default, or any variable passed as the third argument) and return the number of substitutions made — 1 at most for `sub`, unbounded for `gsub`. In the replacement text, `&` stands for the whole match; write `\&` for a literal ampersand.
🏷️ `#functions` `#strings` `#must-know`
### `printf` and `sprintf` — format it yourself
```bash
awk '{printf "%-6s %s %3d\n", $1, $2, $3}' scores.txt   # printf: no automatic newline, no separators — the format string is everything
awk '{print sprintf("%03d", NR), $1}' scores.txt        # sprintf: same formatting, returned as a string instead of printed
```
`print` is the quick tool; `printf` is the precise one — aligned columns (`%-6s` left-pads, `%3d` right-aligns a number), fixed decimals (`%.2f`), zero padding (`%03d`). It adds **no** newline and no field separators: if the output runs together, the format string forgot them.
🏷️ `#functions` `#output` `#must-know`
### `match()` with `RSTART`/`RLENGTH` — find AND extract
```bash
awk '{if (match($0, /job [0-9]+/)) print substr($0, RSTART, RLENGTH)}' app.log   # match() returns where the match starts and sets RSTART/RLENGTH
```
`~` tells you *whether*; `match()` tells you *where* and *how long*: it returns the starting position and sets `RSTART` to the same value and `RLENGTH` to the match's length, so `substr($0, RSTART, RLENGTH)` lifts the matched text out. On no match it returns 0 and sets `RSTART` to 0, `RLENGTH` to −1.
🏷️ `#functions` `#regex` `#strings`
### `toupper()` / `tolower()` / `index()` — small string tools
```bash
awk '{print toupper($1), $3}' scores.txt       # toupper/tolower return a case-folded copy
awk 'index($0, "ERROR") {print}' app.log       # index returns WHERE a substring starts (0 = absent) — as a pattern: "line contains"
```
`index(haystack, needle)` is a plain substring search — position of the first occurrence, in characters — not a regex. Used as a pattern, its 0-for-absent doubles as false, which makes it the readable way to say "contains this literal text".
🏷️ `#functions` `#strings`

---

## 🍳 Recipes — the one-liners people actually keep

### Sum a column
```bash
awk '{s += $10} END {print s}' access.log      # 3008 — total bytes served
```
The accumulator is awk's hello-world: an uninitialized variable starts at 0, every record adds its field, `END` prints the total. Swap in any numeric field and any file.
🏷️ `#recipes` `#sum` `#must-know`
### Average — with the empty-file guard
```bash
awk '{s += $3; n++} END {if (n > 0) print s / n}' scores.txt   # 82.5 — without the if, empty input dies on division by zero
```
Keep a running sum *and* a count, divide once at the end. The `if (n > 0)` looks paranoid until the day the upstream file is empty and the unguarded version errors out — guard every division in `END`.
🏷️ `#recipes` `#average`
### Dedupe lines, keep first-seen order
```bash
awk '!seen[$0]++' words.txt   # first sighting: seen[line] is 0, !0 prints; every repeat is skipped
```
The most famous awk one-liner there is. `seen` is an associative array keyed by the line itself: the first time a line appears, `seen[$0]` is 0 (false), the `!` makes the pattern true, and the default action prints; `++` then records the sighting, so repeats fail the pattern. Unlike `sort -u` it preserves the original order — at the price of holding every unique line in memory.
🏷️ `#recipes` `#dedupe` `#must-know`
### Group-by sum — totals per key
```bash
awk '{tot[$2] += $3} END {for (k in tot) print k, tot[k]}' scores.txt   # totals per subject
```
An associative array turns any field into a bucket: one line of code is a full GROUP BY. ⚠️ `for (k in array)` walks the keys in an unspecified order — pipe the output through `sort` when order matters.
🏷️ `#recipes` `#arrays` `#group-by`
### Word frequency
```bash
awk '{for (i = 1; i <= NF; i++) c[$i]++} END {for (w in c) print c[w], w}' words.txt   # count every word in the file
```
The field loop `for (i = 1; i <= NF; i++)` visits every field of the record; counting into an array is the whole algorithm. Add `| sort -rn` for the ranked list, most frequent first.
🏷️ `#recipes` `#arrays` `#counting`
### Join two files — the `NR == FNR` idiom
```bash
awk 'NR == FNR {tier[$1] = $2; next} {print $1, $2, tier[$1]}' codes.txt events.txt   # load the lookup file first, then stream the data file through it
```
While the first file is being read, `NR` (global count) and `FNR` (per-file count) are still equal — those records are the lookup table, stored and skipped with `next`. From the second file on, `FNR` lags behind and each record is printed with its looked-up value; a key with no entry prints as empty. ⚠️ The idiom breaks if the first file is *empty*: no records are read from it, so `NR == FNR` stays true into the second file and its rows get swallowed as lookup lines.
🏷️ `#recipes` `#join` `#files` `#must-know`
### Pull and reorder columns — CSV in, TSV out
```bash
awk 'BEGIN {FS = ","; OFS = "\t"} NR > 1 {print $3, $1}' people.csv   # city, name — out of the CSV, tab-separated
```
Set both separators in `BEGIN`, then print the fields in any order you like — this is awk's home turf: reshaping clean, simply-delimited data. The next entry is about the unclean kind.
🏷️ `#recipes` `#csv`
### The CSV warning — quotes do not protect commas
```bash
awk -F, '{print NF}' quoted.csv   # 2, 4, 2: the quoted "Doe, John" row explodes into 4 fields — awk cannot see the quotes
```
⚠️ awk has **no CSV parser**: a comma inside `"…"` is a separator like any other, so quoted rows silently split into the wrong number of fields. GNU awk's `FPAT` variable can describe fields by content instead — but it is a gawk extension that mawk and BSD awk *silently ignore* (verified on mawk: setting it changed nothing). For real-world CSV, run a CSV-aware tool first and let awk eat the clean output.
🏷️ `#recipes` `#csv` `#gotcha`
### The longest line
```bash
awk '{if (length($0) > max) {max = length($0); line = $0}} END {print max, line}' app.log   # keep the champion, report at END
```
The "keep the best so far" pattern: a champion variable, a challenger test per record, the verdict in `END`. The same skeleton finds the max value, the newest timestamp, or the worst offender in any column.
🏷️ `#recipes` `#max`

---

## 🧭 awk vs grep vs sed — who does what

| The job | Reach for |
|---|---|
| Print the lines that match a pattern, nothing more | `grep` |
| Swap this text for that text, line by line, in a stream | `sed` |
| Fields, arithmetic, grouping, totals, multi-file joins | `awk` |

`grep` filters without understanding structure — it cannot see columns. `sed` edits a stream beautifully but has no numbers, no arrays, and no per-file counters. `awk` is the one that sees *fields* and remembers things between lines. Real pipelines chain them in that order: `grep` to shrink the haystack, `awk` to do the math.

## ⚠️ Implementation notes — gawk vs mawk vs BusyBox

Every entry above was run and verified on **mawk 1.3.4**. The differences that bite, each verified live unless noted:

- **`gensub()`, `BEGINFILE`/`ENDFILE`, and `FPAT` are GNU awk extensions.** mawk refuses `gensub` loudly ("function gensub never defined") — but it **silently ignores** `BEGINFILE` blocks and `FPAT`: the script runs, the block just never fires and the fields split the default way. Do not count on the trio in BusyBox awk either. To find out which awk you have: `awk --version` (gawk and mawk both answer; the name is in the first line).
- **`length()` counts bytes on mawk, characters on gawk** (in UTF-8 locales) — and `substr()`/`index()` positions follow the same unit, so column math on non-ASCII text silently shifts between implementations. ASCII-only pipelines never notice.
- **Not everything famous is gawk-only.** On this mawk, `nextfile`, whole-array `delete array`, `length(array)`, regex interval expressions like `/a{2,3}/`, and `split(s, a, "")` into single characters all work — each verified against fixtures before this note was written.

## Contributing

Found a wrong command, an outdated flag, or a bad translation? Pull requests are welcome — keep entries to the format above (one-liner / bash block / tags) and **only real, verified commands; when in doubt, leave it out**.

## License

MIT © 2026 Guangyi Zhao. See [LICENSE](LICENSE).
