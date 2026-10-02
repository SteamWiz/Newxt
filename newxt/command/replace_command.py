import os
import yaml
from wizlib.parser import WizParser

from newxt.command import NewxtCommand


class ReplaceCommand(NewxtCommand):
    """Replace text in a file based on YAML instructions"""

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

        # Validate instructions
        if not isinstance(instructions, dict):
            raise ValueError("YAML must be a dictionary")

        if 'search' not in instructions:
            raise ValueError("Missing 'search' in YAML")

        if 'replace' not in instructions:
            raise ValueError("Missing 'replace' in YAML")

        search = instructions['search']
        replace = instructions['replace']

        # Check for blank values
        if not search or (
            isinstance(search, str) and not search.strip()
        ):
            raise ValueError("'search' cannot be blank")

        if not replace or (
            isinstance(replace, str) and not replace.strip()
        ):
            raise ValueError("'replace' cannot be blank")

        # Read file content
        with open(self.file, 'r') as f:
            content = f.read()

        # Replace only first occurrence
        result = content.replace(str(search), str(replace), 1)

        self.status = 'Replacement complete'
        return result
