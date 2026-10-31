"""The version is written in six places; this fails when they drift apart.

meson.build, the PKGBUILD, the RPM spec, the Debian control file, the README
badge and the newest metainfo release. tools/bump-version.py keeps them in step.
"""
import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(name):
    with open(os.path.join(ROOT, name), encoding="utf-8") as f:
        return f.read()


def find(pattern, name):
    match = re.search(pattern, read(name), re.MULTILINE)
    assert match, f"no version found in {name}"
    return match.group(1)


class Version(unittest.TestCase):
    def setUp(self):
        self.version = find(r"^\s*version: '([^']+)',", "meson.build")

    def test_it_looks_like_a_version(self):
        self.assertRegex(self.version, r"^\d+\.\d+\.\d+$")

    def test_the_pkgbuild_agrees(self):
        self.assertEqual(find(r"^pkgver=(\S+)", "pkg/PKGBUILD"), self.version)

    def test_the_deb_and_rpm_agree(self):
        self.assertEqual(find(r"^Version:\s+(\S+)", "packaging/hanuchi.spec"), self.version)
        self.assertEqual(find(r"^Version: (\S+)", "packaging/deb/control"), self.version)

    def test_the_readme_badge_agrees(self):
        self.assertEqual(find(r"badge/release-v([\d.]+)-", "README.md"), self.version)

    def test_the_newest_metainfo_release_agrees(self):
        newest = find(r'<release version="([^"]+)"', "data/com.github.hanuchi.metainfo.xml")
        self.assertEqual(newest, self.version)


if __name__ == "__main__":
    unittest.main()
