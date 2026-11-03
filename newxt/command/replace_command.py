import os
import yaml
from wizlib.parser import WizParser

from newxt.command import NewxtCommand


class ReplaceCommand(NewxtCommand):
    """Replace text in a file based on one or more YAML edit instructions"""

    name = 'replace'

    @classmethod
    def add_args(cls, parser: WizParser):
        super().add_args(parser)
        parser.add_argument(
            'file',
            help='Path to the file to perform replacement on'
        )

    def handle_vals(self):
        super().handle_vals()

    @NewxtCommand.wrap
    def execute(self):
        # Check if file exists
        if not os.path.exists(self.file):
            raise FileNotFoundError(
                f"File not found: {self.file}"
            )

        # Check if path is a directory
        if os.path.isdir(self.file):
            raise IsADirectoryError(
                f"Path is a directory: {self.file}"
            )

        # Get stdin content
        stdin_text = self.app.stream.text
        if not stdin_text or not stdin_text.strip():
            raise ValueError("No stdin provided")

        # Parse YAML
        try:
            instructions = yaml.safe_load(stdin_text)
        except yaml.YAMLError:
            raise ValueError("Invalid YAML in stdin")

        edits = self.parse_edits(instructions)

        # Read file content
        with open(self.file, 'r') as f:
            content = f.read()

        # Apply edits in order, replacing only the first occurrence of each
        for label, search, replace in edits:
            if search not in content:
                raise ValueError(f"{label}'search' text not found")
            content = content.replace(search, replace, 1)

        if len(edits) == 1:
            self.status = 'Replacement complete'
        else:
            self.status = f'{len(edits)} replacements complete'
        return content

    @staticmethod
    def parse_edits(instructions):
        """Return a list of (label, search, replace) tuples from parsed YAML,
        which is either a single edit mapping or a list of them"""
        if isinstance(instructions, dict):
            items = [instructions]
            labelled = False
        elif isinstance(instructions, list):
            if not instructions:
                raise ValueError("YAML list must contain at least one edit")
            items = instructions
            labelled = True
        else:
            raise ValueError("YAML must be a dictionary or a list")

        edits = []
        for index, item in enumerate(items, start=1):
            label = f"Edit {index}: " if labelled else ""
            if not isinstance(item, dict):
                raise ValueError(f"{label}edit must be a dictionary")
            for key in ('search', 'replace'):
                if key not in item:
                    raise ValueError(f"{label}Missing '{key}' in YAML")
                value = item[key]
                if not value or (
                    isinstance(value, str) and not value.strip()
                ):
                    raise ValueError(f"{label}'{key}' cannot be blank")
            edits.append(
                (label, str(item['search']), str(item['replace']))
            )
        return edits
