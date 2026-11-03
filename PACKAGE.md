# Newxt

⚠️ DISCLAIMER: This is a hobby/personal project. Not a commercial product. Not for production use.

## Edit files in one pass with instructions via stdin

The `replace` command performs one or more exact string replacements on a file, in a single pass, based on YAML instructions provided via stdin.

## Quick installation (MacOS)

```bash
brew install pipx
pipx install newxt
```

## Usage

```bash
newxt replace <file> < instructions.yaml
```

Or using a pipe:

```bash
echo "search: old\nreplace: new" | newxt replace myfile.txt
```

## Arguments

- `file` - Path to the file to perform replacement on (required)

## Input Format

The command accepts YAML instructions via stdin: either a single edit (a mapping) or a list of edits. Each edit has two required fields:

- `search` - The text to search for in the file
- `replace` - The text to replace it with

### Simple Example

```yaml
search: old_method
replace: new_method
```

### Multiline Example

For multiline strings, use YAML's literal block scalar syntax:

```yaml
search: |
  def old_method():
    print("old")
replace: |
  def new_method():
    print("new")
```

### Multiple Edits Example

To make several edits in one pass, provide a YAML list of edits:

```yaml
- search: old_method
  replace: new_method
- search: |
    if debug:
      print("Debug mode")
  replace: |
    if self.debug:
      self.logger.debug("Debug mode")
```

## Behavior

- Edits are applied **in order**, each to the result of the previous one
- Each edit replaces only the **first occurrence** of its search string
- The file is **not modified** on disk - the result is returned to stdout
- The search is performed as an exact string match (not a regex)
- Both `search` and `replace` values must be non-empty
- If any edit's search string is not found, the command fails and produces no output

## Error Conditions

The command will raise an error if:

- The specified file does not exist
- The path points to a directory instead of a file
- No stdin is provided
- The stdin is not valid YAML
- The stdin is neither a single edit nor a list of edits, or the list is empty
- The `search` field is missing or blank
- The `replace` field is missing or blank
- The `search` text is not found in the file (after any earlier edits are applied)

When the input is a list, error messages identify the failing edit by its position (e.g. `Edit 2: 'search' text not found`).

## Examples

### Replace a function name

```bash
cat > instructions.yaml << EOF
search: calculate_total
replace: compute_sum
EOF

newxt replace mycode.py < instructions.yaml
```

### Replace a multiline block

```bash
cat > instructions.yaml << EOF
search: |
  if debug:
    print("Debug mode")
replace: |
  if self.debug:
    self.logger.debug("Debug mode")
EOF

newxt replace app.py < instructions.yaml > app_updated.py
```

### Apply several edits at once

```bash
cat > instructions.yaml << EOF
- search: calculate_total
  replace: compute_sum
- search: TODO
  replace: DONE
EOF

newxt replace mycode.py < instructions.yaml
```

### Using with pipes

```bash
echo "search: TODO\nreplace: DONE" | newxt replace notes.txt
```

## Notes

- The command returns the modified content to stdout
- To save the result, redirect the output to a new file
- The original file remains unchanged
- Whitespace and indentation in the search string must match exactly
