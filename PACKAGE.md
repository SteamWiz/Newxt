# Newxt

⚠️ DISCLAIMER: This is a hobby/personal project. Not a commercial product. Not for production use.

## Edit files in one pass with instructions via stdin

The `replace` command performs a simple string replacement on a file based on YAML instructions provided via stdin.

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

The command accepts YAML instructions via stdin with two required fields:

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

## Behavior

- Only the **first occurrence** of the search string is replaced
- The file is **not modified** on disk - the result is returned to stdout
- The search is performed as an exact string match (not a regex)
- Both `search` and `replace` values must be non-empty

## Error Conditions

The command will raise an error if:

- The specified file does not exist
- The path points to a directory instead of a file
- No stdin is provided
- The stdin is not valid YAML
- The `search` field is missing or blank
- The `replace` field is missing or blank

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

### Using with pipes

```bash
echo "search: TODO\nreplace: DONE" | newxt replace notes.txt
```

## Notes

- The command returns the modified content to stdout
- To save the result, redirect the output to a new file
- The original file remains unchanged
- Whitespace and indentation in the search string must match exactly
