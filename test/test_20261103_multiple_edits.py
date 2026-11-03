import os
import tempfile
from wizlib.test_case import WizLibTestCase
from wizlib.stream_handler import StreamHandler

from newxt import NewxtApp
from newxt.command.replace_command import ReplaceCommand


class TestMultipleEdits(WizLibTestCase):

    def run_replace(self, content, instructions):
        with tempfile.NamedTemporaryFile(
            mode='w', delete=False
        ) as f:
            f.write(content)
            p = f.name
        try:
            a = NewxtApp()
            a.stream = StreamHandler()
            a.stream._text = instructions
            c = ReplaceCommand(a, file=p)
            return c.execute(), c
        finally:
            os.unlink(p)

    def test_list_of_edits(self):
        """Test that every edit in a list is applied"""
        r, c = self.run_replace(
            "def old_method():\n    # TODO\n    return 42\n",
            "- search: old_method\n  replace: new_method\n"
            "- search: TODO\n  replace: DONE\n"
        )
        self.assertEqual(
            r, "def new_method():\n    # DONE\n    return 42\n"
        )
        self.assertEqual(c.status, '2 replacements complete')

    def test_edits_applied_in_order(self):
        """Test that each edit sees the result of the previous one"""
        r, _ = self.run_replace(
            "alpha\n",
            "- search: alpha\n  replace: beta\n"
            "- search: beta\n  replace: gamma\n"
        )
        self.assertEqual(r, "gamma\n")

    def test_each_edit_replaces_first_occurrence(self):
        """Test that repeated edits walk through successive occurrences"""
        r, _ = self.run_replace(
            "foo foo foo",
            "- search: foo\n  replace: bar\n"
            "- search: foo\n  replace: baz\n"
        )
        self.assertEqual(r, "bar baz foo")

    def test_multiline_edits(self):
        """Test a list of multiline edits"""
        r, _ = self.run_replace(
            "def a():\n  pass\n\ndef b():\n  pass\n",
            "- search: |\n    def a():\n      pass\n"
            "  replace: |\n    def a():\n      return 1\n"
            "- search: |\n    def b():\n      pass\n"
            "  replace: |\n    def b():\n      return 2\n"
        )
        self.assertEqual(
            r, "def a():\n  return 1\n\ndef b():\n  return 2\n"
        )

    def test_single_item_list(self):
        """Test a list containing one edit"""
        r, c = self.run_replace(
            "hello world", "- search: world\n  replace: there\n"
        )
        self.assertEqual(r, "hello there")
        self.assertEqual(c.status, 'Replacement complete')

    def test_single_mapping_still_supported(self):
        """Test the original single-edit mapping format"""
        r, c = self.run_replace(
            "hello world", "search: world\nreplace: there\n"
        )
        self.assertEqual(r, "hello there")
        self.assertEqual(c.status, 'Replacement complete')

    def test_search_not_found_single(self):
        """Test error when a single edit's search text is absent"""
        with self.assertRaisesRegex(ValueError, "not found"):
            self.run_replace("hello", "search: missing\nreplace: x\n")

    def test_search_not_found_in_list(self):
        """Test error names the edit whose search text is absent"""
        with self.assertRaisesRegex(ValueError, "Edit 2: 'search'"):
            self.run_replace(
                "hello world",
                "- search: hello\n  replace: hi\n"
                "- search: missing\n  replace: x\n"
            )

    def test_search_consumed_by_earlier_edit(self):
        """Test error when an earlier edit removed the later search text"""
        with self.assertRaisesRegex(ValueError, "Edit 2: 'search'"):
            self.run_replace(
                "alpha",
                "- search: alpha\n  replace: beta\n"
                "- search: alpha\n  replace: gamma\n"
            )

    def test_empty_list(self):
        """Test error when the list has no edits"""
        with self.assertRaisesRegex(ValueError, "at least one edit"):
            self.run_replace("hello", "[]\n")

    def test_list_item_not_mapping(self):
        """Test error when a list item is not a mapping"""
        with self.assertRaisesRegex(ValueError, "Edit 2: edit must be"):
            self.run_replace(
                "hello", "- search: hello\n  replace: hi\n- just text\n"
            )

    def test_list_item_missing_replace(self):
        """Test error names the edit missing 'replace'"""
        with self.assertRaisesRegex(
            ValueError, "Edit 2: Missing 'replace'"
        ):
            self.run_replace(
                "hello world",
                "- search: hello\n  replace: hi\n"
                "- search: world\n"
            )

    def test_list_item_blank_search(self):
        """Test error names the edit with a blank 'search'"""
        with self.assertRaisesRegex(
            ValueError, "Edit 1: 'search' cannot be blank"
        ):
            self.run_replace(
                "hello", "- search: ''\n  replace: hi\n"
            )

    def test_scalar_yaml(self):
        """Test error when YAML is neither a mapping nor a list"""
        with self.assertRaisesRegex(ValueError, "dictionary or a list"):
            self.run_replace("hello", "just a string\n")
