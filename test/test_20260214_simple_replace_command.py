import os
import tempfile
from wizlib.test_case import WizLibTestCase
from wizlib.stream_handler import StreamHandler

from newxt import NewxtApp
from newxt.command.replace_command import ReplaceCommand


class TestReplaceCommand(WizLibTestCase):

    def test_basic_replace(self):
        """Test basic string replacement in a file"""
        with tempfile.NamedTemporaryFile(
            mode='w', delete=False
        ) as f:
            f.write("def old_method():\n    return 42\n")
            p = f.name
        try:
            a = NewxtApp()
            a.stream = StreamHandler()
            a.stream._text = "search: old_method\nreplace: new_method"
            c = ReplaceCommand(a, file=p)
            r = c.execute()
            self.assertIn("new_method", r)
            self.assertNotIn("old_method", r)
        finally:
            os.unlink(p)

    def test_multiline_replace(self):
        """Test multiline string replacement"""
        with tempfile.NamedTemporaryFile(
            mode='w', delete=False
        ) as f:
            f.write("def old():\n  print('old')\n")
            p = f.name
        try:
            a = NewxtApp()
            a.stream = StreamHandler()
            a.stream._text = (
                "search: |\n  def old():\n    print('old')\n"
                "replace: |\n  def new():\n    print('new')\n"
            )
            c = ReplaceCommand(a, file=p)
            r = c.execute()
            self.assertIn("def new():", r)
            self.assertIn("print('new')", r)
            self.assertNotIn("old", r)
        finally:
            os.unlink(p)

    def test_only_first_occurrence(self):
        """Test that only first occurrence is replaced"""
        with tempfile.NamedTemporaryFile(
            mode='w', delete=False
        ) as f:
            f.write("foo\nfoo\nfoo\n")
            p = f.name
        try:
            a = NewxtApp()
            a.stream = StreamHandler()
            a.stream._text = "search: foo\nreplace: bar"
            c = ReplaceCommand(a, file=p)
            r = c.execute()
            self.assertEqual(r.count("bar"), 1)
            self.assertEqual(r.count("foo"), 2)
        finally:
            os.unlink(p)

    def test_file_not_found(self):
        """Test error when file doesn't exist"""
        a = NewxtApp()
        a.stream = StreamHandler()
        a.stream._text = "search: foo\nreplace: bar"
        c = ReplaceCommand(a, file="/nonexistent/file.txt")
        with self.assertRaises(FileNotFoundError):
            c.execute()

    def test_path_is_directory(self):
        """Test error when path is a directory"""
        with tempfile.TemporaryDirectory() as d:
            a = NewxtApp()
            a.stream = StreamHandler()
            a.stream._text = "search: foo\nreplace: bar"
            c = ReplaceCommand(a, file=d)
            with self.assertRaises(IsADirectoryError):
                c.execute()

    def test_no_stdin(self):
        """Test error when no stdin provided"""
        with tempfile.NamedTemporaryFile(
            mode='w', delete=False
        ) as f:
            f.write("content")
            p = f.name
        try:
            a = NewxtApp()
            a.stream = StreamHandler()
            a.stream._text = ""
            c = ReplaceCommand(a, file=p)
            with self.assertRaises(ValueError):
                c.execute()
        finally:
            os.unlink(p)

    def test_invalid_yaml(self):
        """Test error when stdin is not valid YAML"""
        with tempfile.NamedTemporaryFile(
            mode='w', delete=False
        ) as f:
            f.write("content")
            p = f.name
        try:
            a = NewxtApp()
            a.stream = StreamHandler()
            a.stream._text = "not: yaml: invalid:"
            c = ReplaceCommand(a, file=p)
            with self.assertRaises(ValueError):
                c.execute()
        finally:
            os.unlink(p)

    def test_missing_search(self):
        """Test error when search is missing"""
        with tempfile.NamedTemporaryFile(
            mode='w', delete=False
        ) as f:
            f.write("content")
            p = f.name
        try:
            a = NewxtApp()
            a.stream = StreamHandler()
            a.stream._text = "replace: bar"
            c = ReplaceCommand(a, file=p)
            with self.assertRaises(ValueError):
                c.execute()
        finally:
            os.unlink(p)

    def test_blank_search(self):
        """Test error when search is blank"""
        with tempfile.NamedTemporaryFile(
            mode='w', delete=False
        ) as f:
            f.write("content")
            p = f.name
        try:
            a = NewxtApp()
            a.stream = StreamHandler()
            a.stream._text = "search: \nreplace: bar"
            c = ReplaceCommand(a, file=p)
            with self.assertRaises(ValueError):
                c.execute()
        finally:
            os.unlink(p)

    def test_missing_replace(self):
        """Test error when replace is missing"""
        with tempfile.NamedTemporaryFile(
            mode='w', delete=False
        ) as f:
            f.write("content")
            p = f.name
        try:
            a = NewxtApp()
            a.stream = StreamHandler()
            a.stream._text = "search: foo"
            c = ReplaceCommand(a, file=p)
            with self.assertRaises(ValueError):
                c.execute()
        finally:
            os.unlink(p)

    def test_blank_replace(self):
        """Test error when replace is blank"""
        with tempfile.NamedTemporaryFile(
            mode='w', delete=False
        ) as f:
            f.write("content")
            p = f.name
        try:
            a = NewxtApp()
            a.stream = StreamHandler()
            a.stream._text = "search: foo\nreplace: "
            c = ReplaceCommand(a, file=p)
            with self.assertRaises(ValueError):
                c.execute()
        finally:
            os.unlink(p)

    def test_file_not_modified(self):
        """Test that file is not modified on disk"""
        with tempfile.NamedTemporaryFile(
            mode='w', delete=False
        ) as f:
            f.write("original content")
            p = f.name
        try:
            a = NewxtApp()
            a.stream = StreamHandler()
            a.stream._text = "search: original\nreplace: modified"
            c = ReplaceCommand(a, file=p)
            c.execute()
            with open(p, 'r') as f:
                content = f.read()
            self.assertEqual(content, "original content")
        finally:
            os.unlink(p)
