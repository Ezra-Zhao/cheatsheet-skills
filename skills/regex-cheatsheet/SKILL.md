---
name: regex-cheatsheet
description: 'Use when the user needs regular expressions: character classes, anchors, quantifiers, groups and backreferences, lookahead and lookbehind, ready-made patterns for emails, URLs, dates and IP addresses, and syntax differences between grep, sed, Python, JavaScript and PCRE.'
---

# Regex Cheatsheet — Patterns That Actually Work

One page. Thirty entries. Each tells you **what it matches**, gives you **a copy-paste pattern**, and tags the use case. Based on syntax shared by PCRE / Python / JavaScript — engine differences are called out where they matter.

> 🌍 Read this project in your language: [中文](README.md) · [Español](README.es.md) · [Português](README.pt.md)

Test every pattern at https://regex101.com/ (pick the right engine: PCRE2 / Python / JavaScript).

---

## 🔤 Basic metacharacters

### `.` — any character except a newline
The wildcard. Matches letters, digits, punctuation — anything but `\n` (unless DOTALL/single-line mode is on).
```regex
a.c
# matches: abc, a1c, a-c … but not "ac" or "a\nc"
```
🏷️ `#basics` `#wildcard`

### `\d` / `\D` — digit / non-digit
`\d` is shorthand for `[0-9]`; `\D` is its exact opposite (`[^0-9]`). The uppercase version always negates the lowercase one — this rule holds for `\w`/`\W` and `\s`/`\S` too.
```regex
Order \d+
# matches "Order 42" — one or more digits
```
🏷️ `#basics` `#shorthand`

### `\w` / `\W` — word character / non-word character
`\w` = `[A-Za-z0-9_]` (letters, digits, underscore). Handy for identifiers, usernames, tokens.
```regex
\w+
# matches "user_1", "abc", "007" — stops at spaces and punctuation
```
🏷️ `#basics` `#shorthand`

### `\s` / `\S` — whitespace / non-whitespace
`\s` matches space, tab, newline, carriage return, form feed. `\S` matches everything else.
```regex
Hello\sWorld
# matches "Hello World", "Hello\tWorld"
```
🏷️ `#basics` `#shorthand`

### `^` `$` — start / end anchors
`^` anchors to the start, `$` to the end. Without the multiline flag they mean start/end of the whole string; with multiline (`m`), start/end of each line.
```regex
^Hello
# matches only if the string/line starts with "Hello"
\d+$
# matches only if the string/line ends with digits
```
🏷️ `#basics` `#anchors`

### `\b` — word boundary
Matches the invisible edge between a word character and a non-word character. The classic way to match whole words only.
```regex
\bcat\b
# matches "cat" but not "cats", "concat", or "educate"
```
🏷️ `#basics` `#boundaries`

---

## 🔁 Quantifiers

### `*` `+` `?` — zero-or-more / one-or-more / optional
The three you'll use 90% of the time.
```regex
https?://
# "http://" or "https://" — the s is optional
\d+
# one or more digits: "5", "42", "007"
colou?r
# "color" or "colour"
```
🏷️ `#quantifiers` `#basics`

### `{n}` `{n,}` `{n,m}` — exact / at-least / range counts
Precise repetition when `*`/`+`/`?` aren't specific enough.
```regex
\d{3}-\d{4}
# "555-1234" — exactly 3 digits, dash, exactly 4 digits
\d{2,}
# at least 2 digits
[a-z]{4,8}
# 4 to 8 lowercase letters (e.g. a username rule)
```
🏷️ `#quantifiers` `#counts`

### Greedy vs lazy — `.*` vs `.*?`
Quantifiers are **greedy** by default: they grab as much as possible. Add `?` to make them **lazy**: stop at the first possible match.
```regex
<.*>
# greedy: on "<b>hi</b>" matches the whole "<b>hi</b>"
<.*?>
# lazy: on "<b>hi</b>" matches "<b>" then "</b>" separately
```
🏷️ `#quantifiers` `#greedy` · Note: possessive quantifiers (`*+`, `++`) exist in PCRE/Java but **not** in Python or JavaScript.

---

## 🧩 Character classes & alternation

### `[...]` — character class
Match any single character from the set. Ranges with `-`; most metacharacters lose their magic inside (`.` is literal, but `]` `\` `^` `-` still need care).
```regex
[aeiou]
# any single vowel
[a-zA-Z]
# any single letter
gr[ae]y
# "gray" or "grey"
```
🏷️ `#classes` `#sets`

### `[^...]` — negated character class
Match any single character **not** in the set. The `^` only means "not" when it's the first character inside the brackets.
```regex
[^0-9]
# same as \D — any non-digit
[^<>]*
# any run of characters that aren't angle brackets
```
🏷️ `#classes` `#negation`

### `|` — alternation (OR)
Match this **or** that. Has the lowest precedence of all — use `(...)` to limit its scope.
```regex
cat|dog
# "cat" or "dog"
gr(a|e)y
# "gray" or "grey" — the | only applies inside the group
```
🏷️ `#alternation` `#branching`

---

## 📦 Groups & capturing

### `(...)` — capturing group
Groups a sub-pattern (for quantifiers or `|`) **and** remembers what it matched, numbered from 1 left to right.
```regex
(\d{3})-(\d{4})
# group 1 = area code, group 2 = number
(ha)+
# "ha", "haha", "hahaha" — quantifier applies to the group
```
🏷️ `#groups` `#capturing`

### `(?<name>...)` — named capturing group
Same as `(...)` but the match is also retrievable by name — far more readable than `$7`.
```regex
(?<year>\d{4})-(?<month>\d{2})
# year="2026", month="10"
```
🏷️ `#groups` `#named` · Python also accepts `(?P<name>...)`; JavaScript needs ES2018+.

### `(?:...)` — non-capturing group
Groups without remembering — use it when you need grouping for `|` or a quantifier but don't want an extra capture slot.
```regex
(?:https?://)?[\w.-]+
# optional scheme, not captured — keeps group numbers clean
```
🏷️ `#groups` `#performance`

### Backreferences — `\1` inside the pattern
Match the exact same text a previous group captured. The classic paired-quote matcher.
```regex
(['"]).*?\1
# "hello" or 'hello' — closing quote must match the opening one
(\w+)\s+\1
# repeated word: "the the"
```
🏷️ `#groups` `#backreference`

---

## 👀 Lookaround assertions

### `(?=...)` — positive lookahead
Asserts "what follows must be X" **without consuming** it. The lookahead itself matches zero characters.
```regex
\d+(?= dollars)
# matches "100" in "100 dollars" — " dollars" stays for later
^(?=.*[A-Z])(?=.*\d).{8,}$
# password: 8+ chars, at least one uppercase and one digit
```
🏷️ `#assertions` `#lookahead`

### `(?!...)` — negative lookahead
Asserts "what follows must NOT be X". Great for exclusions.
```regex
foo(?!bar)
# "foo" not followed by "bar" — matches "food", "fool", not "foobar"
```
🏷️ `#assertions` `#lookahead`

### `(?<=...)` — positive lookbehind
Asserts "what precedes must be X" without consuming it. Looks backwards.
```regex
(?<=\$)\d+
# matches "42" in "$42" — the $ itself is not part of the match
```
🏷️ `#assertions` `#lookbehind` · JavaScript needs ES2018+; older Safari lacks it.

### `(?<!...)` — negative lookbehind
Asserts "what precedes must NOT be X".
```regex
(?<!not )good
# "good" in "very good" but not in "not good"
```
🏷️ `#assertions` `#lookbehind` · Python's `re` requires fixed-width lookbehind (no `+`/`*` inside); PCRE is more lenient.

---

## 🛠️ Real-world patterns

### Email (loose, practical)
No regex validates email perfectly (the RFC is absurd); this catches real-world addresses without false rejections.
```regex
[\w.+-]+@[\w-]+\.[\w.]+
# matches: name@example.com, first.last+tag@sub.domain.co
```
🏷️ `#recipes` `#email` `#validation`

### URL (loose, practical)
Good enough for finding links in text — not for security validation.
```regex
https?://[^\s/$.?#].[^\s]*
# matches: https://example.com/path?q=1, http://x.io
```
🏷️ `#recipes` `#url`

### International phone number (loose)
A tolerant pattern for E.164-style numbers with optional formatting characters.
```regex
\+?[1-9]\d{6,14}
# matches: +14155552671, 8613800138000 — validate properly server-side
```
🏷️ `#recipes` `#phone`

### IPv4 address (strict)
Each octet is genuinely 0–255 — the loose `\d{1,3}(\.\d{1,3}){3}` would accept "999.999.999.999".
```regex
((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)
# matches: 192.168.1.1 — rejects 256.1.1.1
```
🏷️ `#recipes` `#ipv4` `#networking`

### Date YYYY-MM-DD (format check)
Checks the shape, not the calendar — "2026-13-99" still matches; validate real dates in code.
```regex
\d{4}-\d{2}-\d{2}
# matches: 2026-10-09
```
🏷️ `#recipes` `#date`

### HTML tag (quick-and-dirty only)
Fine for a rough scrape; see the "don't parse HTML with regex" warning below before using this in production.
```regex
<[^>]+>
# matches: <p>, </div>, <a href="x">
```
🏷️ `#recipes` `#html` `#scraping`

### Trim leading/trailing whitespace
The classic two-anchor alternation, used with a replace-by-empty-string.
```regex
^\s+|\s+$
# replace matches with "" → "  hi  " becomes "hi"
```
🏷️ `#recipes` `#trim` `#cleanup`

---

## 🔄 Replacement tricks

### Backreferences in replacements — `$1` vs `\1`
In the **pattern** you always write `\1`; in the **replacement string** it depends on the engine: JavaScript/Python use `$1` (or `\g<1>` in Python), while `sed`/Vim use `\1`.
```regex
pattern:     (\w+)@(\w+)
replacement: $1 at $2
# "user@host" → "user at host" (JS/Python style)
```
```bash
echo "user@host" | grep -P -o '\w+@\w+'   # grep -P = PCRE in the terminal
```
🏷️ `#replacement` `#backreference` · Case-conversion escapes (`\U`, `\L`, `\E`) work in PCRE/Perl/Vim but **not** in Python or JavaScript.

---

## ⚠️ Pitfalls

### Catastrophic backtracking
Nested quantifiers like `(a+)+$` can take longer than the age of the universe on non-matching input — the engine tries exponentially many paths. Fix it with atomic groups `(?>...)` (PCRE/Java) or by rewriting the pattern to be specific.
```regex
(a+)+$
# DANGER: on "aaaaaaaaaaaaaaaaaaaaaaaaaaaaa!" this hangs
(a+)$
# safe: one quantifier, linear time
```
🏷️ `#pitfalls` `#performance` `#redos`

### Don't parse HTML with regex
HTML is not a regular language — nested tags, comments, CDATA and malformed markup will defeat any pattern eventually. Use a real parser: BeautifulSoup (Python), cheerio (JS), or Go's `x/net/html`.
```regex
# <[^>]+> is fine for a quick grep — it is NOT an HTML parser
```
🏷️ `#pitfalls` `#html` `#wisdom`

---

## 📚 Learn more

- Test patterns live: https://regex101.com/ (remember to pick your engine)
- `grep -P` for PCRE regex in the terminal; `man pcrepattern` for the full syntax

## Contributing

Found a wrong pattern, a better recipe, or a bad translation? Pull requests are welcome — keep entries to the format above (what it matches / pattern / tags) and **verify every pattern on regex101 with the matching engine before submitting**.

## License

MIT © 2026 Guangyi Zhao. See [LICENSE](LICENSE).
