"""Package CLI acceptance in temporary fixtures; no skill code is executed."""
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "package.py"


class PackageCLI(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="skill-package-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "scripts").mkdir()
        shutil.copyfile(SCRIPT, self.root / "scripts" / "package.py")
        for platform in ("skills", "chatgpt"):
            (self.root / platform).mkdir()
            self.skill(platform, "valid")

    def skill(self, platform, name):
        folder = self.root / platform / name
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "SKILL.md").write_text("---\nname: valid\ndescription: fixture\n---\n", encoding="utf-8")
        (folder / "asset.txt").write_text("fixture asset", encoding="utf-8")
        return folder

    def run_cli(self, *args):
        return subprocess.run([sys.executable, "-B", "scripts/package.py", *args],
                              cwd=self.root, capture_output=True, text=True)

    def assert_rejected(self, *args):
        result = self.run_cli(*args)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertFalse((self.root / "dist").exists())

    def test_unknown_skill_fails_without_empty_archives(self):
        self.assert_rejected("missing")

    def test_directory_without_skill_document_is_rejected(self):
        (self.root / "skills" / "incomplete").mkdir()
        self.assert_rejected("incomplete")

    def test_parent_path_cannot_package_an_existing_outside_directory(self):
        self.skill(".", "outside")
        self.assert_rejected("../outside")

    def test_names_must_be_single_nonempty_components(self):
        for name in ("", ".", "..", "nested/name", "nested\\name", str(self.root)):
            with self.subTest(name=name):
                self.assert_rejected(name)

    def test_bad_later_name_does_not_replace_an_existing_archive(self):
        path = self.root / "dist" / "claude" / "valid.zip"
        path.parent.mkdir(parents=True)
        path.write_bytes(b"previous artifact")
        result = self.run_cli("valid", "missing")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(path.read_bytes(), b"previous artifact")
        self.assertEqual(list((self.root / "dist").rglob("*.zip")), [path])

    def test_missing_second_platform_is_checked_before_any_write(self):
        shutil.rmtree(self.root / "chatgpt" / "valid")
        self.assert_rejected("valid")

    def test_valid_archive_contains_the_skill_and_asset(self):
        result = self.run_cli("valid")
        self.assertEqual(result.returncode, 0, result.stderr)
        for platform in ("claude", "chatgpt"):
            with zipfile.ZipFile(self.root / "dist" / platform / "valid.zip") as archive:
                self.assertEqual(sorted(archive.namelist()), ["valid/SKILL.md", "valid/asset.txt"])
                self.assertEqual(archive.read("valid/asset.txt"), b"fixture asset")

    def test_only_selected_platform_needs_the_requested_skill(self):
        shutil.rmtree(self.root / "skills" / "valid")
        result = self.run_cli("valid", "--only", "chatgpt")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.root / "dist" / "chatgpt" / "valid.zip").is_file())
        self.assertFalse((self.root / "dist" / "claude").exists())

    def test_default_build_packages_all_discovered_skills(self):
        self.skill("skills", "second")
        self.skill("chatgpt", "second")
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        archives = list((self.root / "dist").rglob("*.zip"))
        self.assertEqual(len(archives), 4)
        for path in archives:
            with zipfile.ZipFile(path) as archive:
                self.assertIn(path.stem + "/SKILL.md", archive.namelist())


if __name__ == "__main__":
    unittest.main()
