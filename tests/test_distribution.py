import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('distribution', ROOT / 'scripts/check_distribution.py')
distribution = importlib.util.module_from_spec(spec)
spec.loader.exec_module(distribution)


class DistributionTests(unittest.TestCase):
    def test_package_is_self_contained_after_relocation(self):
        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory) / 'skills-package'
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns('.git', '__pycache__', '*.pyc'))
            self.assertEqual(distribution.validate(copy), [])

    def test_missing_reference_is_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory) / 'package'
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns('.git', '__pycache__', '*.pyc'))
            (copy / 'skills/1panel-apps/references/tools.md').unlink()
            self.assertTrue(any('tools.md' in item for item in distribution.validate(copy)))

    def test_manifest_cannot_hide_an_unregistered_skill(self):
        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory) / 'package'
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns('.git', '__pycache__', '*.pyc'))
            manifest = copy / '.claude-plugin/plugin.json'
            data = json.loads(manifest.read_text(encoding='utf-8'))
            data['skills'].pop()
            manifest.write_text(json.dumps(data), encoding='utf-8')
            self.assertTrue(any('inventory' in item for item in distribution.validate(copy)))


if __name__ == '__main__':
    unittest.main()
