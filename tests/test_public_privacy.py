"""Privacy checks must inspect removed content and metadata without echoing it."""
import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "tools" / "check_public_privacy.py"
spec = importlib.util.spec_from_file_location("public_privacy", SOURCE)
privacy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(privacy)


class PublicPrivacyTests(unittest.TestCase):
    def test_synthetic_and_public_identities(self):
        self.assertEqual(privacy.categories("author <person@example.com>"), [])
        self.assertEqual(privacy.categories("author <123+account@users.noreply.github.com>"), [])
        self.assertEqual(privacy.categories("/home/" + "operator/project"), [])

    def test_private_contact_and_regex_literal(self):
        contact = "person" + "@" + "mail-provider.com"
        self.assertIn("contact_email", privacy.categories(contact))
        self.assertIn("contact_email", privacy.categories(contact.replace(".", r"\.")))

    def test_local_path_and_private_branch(self):
        self.assertIn("local_user_path", privacy.categories("/home/" + "person_x/project"))
        self.assertIn("local_user_path", privacy.categories("C:/Users/" + "person_x/project"))
        self.assertIn("private_branch_reference", privacy.categories("private/" + "contact_package"))

    def test_encoded_identifier_and_real_key_shape(self):
        encoded = "b64decode(" + repr("cHJpdmF0ZV9pZGVudGlmaWVy") + ")"
        self.assertIn("encoded_literal_review", privacy.categories(encoded))
        self.assertIn("credential_shape", privacy.categories("ghp_" + "a" * 36))
        self.assertEqual(privacy.categories("BEGIN OPENSSH PRIVATE KEY"), [])

    def test_removed_content_stays_visible_in_history(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            def git(*args):
                return subprocess.check_output(["git", "-C", directory, *args], stderr=subprocess.PIPE)
            git("init", "-q")
            git("config", "user.name", "Synthetic author")
            git("config", "user.email", "author@example.com")
            (repo / "sample.txt").write_text("/home/" + "person_x/project\n")
            git("add", "sample.txt")
            git("commit", "-qm", "Add synthetic example")
            (repo / "sample.txt").write_text("generalized example\n")
            git("add", "sample.txt")
            git("commit", "-qm", "Generalize example")
            head_findings, _ = privacy.scan(repo, "HEAD", False)
            self.assertEqual(head_findings, [])
            all_findings, coverage = privacy.scan(repo, "HEAD", True)
            self.assertEqual(coverage["commits"], 2)
            self.assertTrue(any(f["category"] == "local_user_path" for f in all_findings))
            self.assertNotIn("person_x", repr(all_findings))

    def test_author_metadata_is_not_ignored(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            def git(*args):
                return subprocess.check_output(["git", "-C", directory, *args], stderr=subprocess.PIPE)
            git("init", "-q")
            git("config", "user.name", "Synthetic author")
            git("config", "user.email", "person" + "@" + "mail-provider.com")
            git("commit", "--allow-empty", "-qm", "Synthetic metadata")
            findings, _ = privacy.scan(repo, "HEAD", False)
            self.assertTrue(any(f["category"] == "contact_email" for f in findings))

    def test_invalid_revision_does_not_report_clean(self):
        with tempfile.TemporaryDirectory() as directory:
            subprocess.run(["git", "init", "-q", directory], check=True)
            with self.assertRaises(subprocess.SubprocessError):
                privacy.scan(Path(directory), "missing", True)
