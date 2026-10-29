---
name: jq-cheatsheet
description: 'Use when the user needs jq commands: parsing and filtering JSON, selecting and renaming fields, arrays and iteration, constructing new JSON, raw string output, slurp mode, and processing API responses, config files or JSON logs.'
---

# jq Cheatsheet — Command-Line JSON Processing

One page. 30 filters. Each entry tells you **what it does** and gives you a **copy-paste filter that really works** — every filter below was executed against real data with jq 1.7 before being published.

> 🌍 Read this project in your language: [中文](README.md) · [Español](README.es.md) · [Português](README.pt.md)

Docs: https://jqlang.github.io/jq/manual/

Install: `brew install jq` (macOS) or `sudo apt install jq` (Debian/Ubuntu). A sample `config.json` you can copy-paste to follow along is at the bottom of this page.

---

## 📥 Basics

### Pretty-print any JSON
The reason jq exists: turn a one-line JSON blob into readable, indented output.
```bash
jq '.' config.json
# input:  {"name":"api-server","port":8080}
# output: {
#           "name": "api-server",
#           "port": 8080
#         }
```
🏷️ `#basics` `#pretty-print`

### Extract one field
Dot plus key name pulls the value out. Strings come back quoted — that's normal JSON.
```bash
jq '.name' config.json
# input:  {"name":"api-server","port":8080}
# output: "api-server"
```
🏷️ `#basics` `#extract`

### Raw output: strings without quotes (`-r`)
Use `-r` whenever the result feeds into another shell command — no quotes, no escaping.
```bash
jq -r '.name' config.json
# output: api-server
```
🏷️ `#basics` `#shell` `#must-know`

### Compact output: one object per line (`-c`)
`--compact-output` puts each result on a single line — the format log pipelines love.
```bash
jq -c '.users' config.json
# output: [{"name":"ana","age":28},{"name":"bruno","age":17},{"name":"carla","age":34}]
```
🏷️ `#basics` `#logs` `#pipelines`

---

## 🧭 Navigate nested data & arrays

### Drill into nested objects
Chain keys with dots to walk down any depth.
```bash
jq '.owner.email' config.json
# input:  {"owner":{"name":"Ezra","email":"ezra@example.com"}}
# output: "ezra@example.com"
```
🏷️ `#navigate` `#nested`

### Index into arrays
`[0]` is the first element, `[-1]` the last — then keep navigating with dots.
```bash
jq '.users[0].name' config.json   # first user's name  -> "ana"
jq '.users[-1].name' config.json  # last user's name   -> "carla"
```
🏷️ `#navigate` `#arrays`

### Stream every array element (`.[]`)
`.[]` explodes an array into a stream of values; pipe each one somewhere useful.
```bash
jq -r '.users[].name' config.json
# output: ana
#         bruno
#         carla
```
🏷️ `#navigate` `#arrays` `#iteration`

### Count things (`length`)
`length` works on arrays (element count), strings (characters), and objects (keys).
```bash
jq '.users | length' config.json   # -> 3
jq '.name | length' config.json    # -> 10  (characters in "api-server")
```
🏷️ `#navigate` `#count`

---

## 🔎 Filter rows with `select`

### Keep rows matching a number condition
`select()` passes through only the values where the expression is true.
```bash
jq -r '.users[] | select(.age >= 18) | .name' config.json
# output: ana
#         carla        (bruno is 17, filtered out)
```
🏷️ `#filter` `#select`

### Match strings exactly
String comparison with `==` — remember the quotes inside the filter.
```bash
jq -r '.users[] | select(.role == "admin") | .name' config.json
# output: ana
```
🏷️ `#filter` `#select`

### Combine conditions: `and`, `or`, `not`
Boolean logic reads like English; `not` negates any filter.
```bash
jq -r '.users[] | select(.age > 18 and .active) | .name' config.json
# output: ana        (carla is inactive, bruno is 17)
jq -r '.users[] | select(.active | not) | .name' config.json
# output: carla
```
🏷️ `#filter` `#select` `#logic`

---

## 🔄 Reshape arrays with `map`

### Pluck one field from every element
`map(f)` runs `f` on each element and collects the results back into an array.
```bash
jq '.users | map(.name)' config.json
# output: ["ana","bruno","carla"]
```
🏷️ `#transform` `#map`

### Reshape objects: keep only some fields
`{name, city}` is shorthand for `{name: .name, city: .city}` — build leaner objects.
```bash
jq -c '.users | map({name, city})' config.json
# output: [{"name":"ana","city":"madrid"},{"name":"bruno","city":"lisboa"},{"name":"carla","city":"madrid"}]
```
🏷️ `#transform` `#map` `#reshape`

### Add a computed field to every element
`. + {...}` merges the new field into each object — originals stay untouched.
```bash
jq -c '.users | map(. + {senior: (.age >= 30)}) | .[2]' config.json
# output: {"name":"carla","age":34,"role":"user","active":false,"city":"madrid","score":88,"senior":true}
```
🏷️ `#transform` `#map` `#computed`

---

## 🔗 Chain with pipes & build objects

### Chain filters with `|`
The pipe feeds the left side's output into the right side's input — compose freely.
```bash
jq -c '.users | map(select(.active)) | map(.name)' config.json
# output: ["ana","bruno"]      (filter first, then pluck)
```
🏷️ `#pipes` `#compose` `#must-know`

### Build an object with shorthand syntax
`{name, age}` inside a filter means `{name: .name, age: .age}` — pick fields fast.
```bash
jq '.users[0] | {name, age}' config.json
# output: { "name": "ana", "age": 28 }
```
🏷️ `#construct` `#objects`

### Build a summary object from many places
Mix literals, paths, and sub-expressions (in parentheses) into one new object.
```bash
jq '. | {app: .name, owner_email: .owner.email, user_count: (.users | length)}' config.json
# output: { "app": "api-server", "owner_email": "ezra@example.com", "user_count": 3 }
```
🏷️ `#construct` `#objects` `#summary`

---

## 🔤 Strings & numbers

### Convert types: `tostring` / `tonumber`
APIs are inconsistent — normalize a field's type before comparing or concatenating.
```bash
jq '.users | map(.age | tostring)' config.json
# output: ["28","17","34"]
echo '"42"' | jq 'tonumber + 8'
# output: 50
```
🏷️ `#strings` `#types`

### Split & join strings
`split` turns a string into an array; `join` glues an array back with a separator.
```bash
echo '"a,b,c"' | jq 'split(",")'        # -> ["a","b","c"]
jq -n -r '["a","b","c"] | join("; ")'   # -n = null input; -> a; b; c
```
🏷️ `#strings` `#split` `#join`

### Regex match with `test()`
`test("pattern")` is true when the string matches — great inside `select()`.
```bash
jq -r '.users[] | select(.name | test("^a")) | .name' config.json
# output: ana        (names starting with "a")
```
🏷️ `#strings` `#regex` `#filter`

---

## 📊 Aggregate

### Sort by a field
`sort_by(f)` orders objects by `f`; plain `sort` works on simple arrays.
```bash
jq '.users | sort_by(.age) | map(.name)' config.json
# output: ["bruno","ana","carla"]      (17, 28, 34)
```
🏷️ `#aggregate` `#sort`

### Deduplicate with `unique`
`unique` sorts and removes duplicates — feed it a plucked array.
```bash
jq '.users | map(.city) | unique' config.json
# output: ["lisboa","madrid"]
```
🏷️ `#aggregate` `#dedupe`

### Group & count with `group_by`
`group_by(f)` clusters equal values; each group keeps its members for counting.
```bash
jq -c '.users | group_by(.city) | map({city: .[0].city, count: length})' config.json
# output: [{"city":"lisboa","count":1},{"city":"madrid","count":2}]
```
🏷️ `#aggregate` `#group` `#count`

### Sum with `add`
`add` sums an array of numbers (it also concatenates arrays and merges objects).
```bash
jq '.users | map(.score) | add' config.json
# output: 255      (92 + 75 + 88)
```
🏷️ `#aggregate` `#sum`

### Top / bottom by a field
`max_by(f)` and `min_by(f)` return the whole winning object, not just the value.
```bash
jq '.users | max_by(.score) | {name, score}' config.json
# output: { "name": "ana", "score": 92 }
jq '.users | min_by(.age) | {name, age}' config.json
# output: { "name": "bruno", "age": 17 }
```
🏷️ `#aggregate` `#max` `#min`

---

## 🗝️ Inspect & trim keys

### List keys, test presence, delete fields
`keys` shows an object's keys, `has()` tests one, `del()` returns the object minus a field.
```bash
jq '.users[0] | keys' config.json
# output: ["active","age","city","name","role","score"]
jq '.users[0] | has("role")' config.json   # -> true
jq -c 'del(.debug) | keys' config.json
# output: ["name","owner","port","tags","users","version"]   (debug gone)
```
🏷️ `#objects` `#keys` `#cleanup`

---

## 🛠️ Real world

### API in, answers out: `curl | jq`
The classic one-liner — fetch JSON from any API and shape it on the spot.
```bash
curl -s https://api.github.com/repos/jqlang/jq | jq '{stars: .stargazers_count, forks: .forks_count}'
# output: { "stars": 21000, "forks": 1500 }
```
🏷️ `#realworld` `#api` `#must-know`

### Count log levels in a JSON log file
`-r` gives plain text, then standard Unix tools finish the job.
```bash
jq -r '.level' app.log | sort | uniq -c
# output:   2 error
#           2 info
```
🏷️ `#realworld` `#logs` `#devops`

### Pass a shell variable into jq (`--arg`)
Never interpolate `$VAR` into the filter string (injection risk) — use `--arg`.
```bash
jq --arg v "2.4.1" '.version = $v' config.json | jq '.version'
# output: "2.4.1"
```
🏷️ `#realworld` `#shell` `#safe`

### Slurp many JSON docs into one (`-s`)
`--slurp` reads a stream of JSON values into an array; `add` merges objects.
```bash
printf '%s\n' '{"a":1}' '{"b":2}' | jq -s '.'
# output: [ { "a": 1 }, { "b": 2 } ]
printf '%s\n' '{"a":1}' '{"b":2}' | jq -s 'add'
# output: { "a": 1, "b": 2 }
```
🏷️ `#realworld` `#slurp` `#merge`

---

## 🧪 Sample data — try everything above

Save as `config.json`, then run any filter from this page against it:
```json
{
  "name": "api-server",
  "version": "2.4.1",
  "port": 8080,
  "debug": false,
  "owner": { "name": "Ezra", "email": "ezra@example.com" },
  "users": [
    {"name": "ana", "age": 28, "role": "admin", "active": true, "city": "madrid", "score": 92},
    {"name": "bruno", "age": 17, "role": "user", "active": true, "city": "lisboa", "score": 75},
    {"name": "carla", "age": 34, "role": "user", "active": false, "city": "madrid", "score": 88}
  ],
  "tags": ["web", "api", "v2"]
}
```

## Reference

Official manual: https://jqlang.github.io/jq/manual/

## Contributing

Found a wrong filter, a missing scenario, or a bad translation? Pull requests are welcome — keep entries to the format above (heading / one line / code block / tags) and **run every filter against real data before submitting**.

## License

MIT © 2026 Guangyi Zhao. See [LICENSE](LICENSE).
