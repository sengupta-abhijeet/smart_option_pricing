#!/usr/bin/env python

"""Tests for `smart_option_pricing` package."""


import unittest

from smart_option_pricing import smart_option_pricing


class TestSmart_option_pricing(unittest.TestCase):
    """Tests for `smart_option_pricing` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

def test_create_project_call_extension_hooks(tmpfolder, git_mock):
    # Given an extension with hooks,
    called = []

    def pre_hook(struct, opts):
        called.append("pre_hook")
        return struct, opts

    def post_hook(struct, opts):
        called.append("post_hook")
        return struct, opts

    # when created project is called,
    create_project(
        project_path="proj", extensions=[create_extension(pre_hook, post_hook)]
    )

    # then the hooks should also be called.
    assert "pre_hook" in called
    assert "post_hook" in called


def test_create_project_generate_extension_files(tmpfolder, git_mock):
    # Given a blank state,
    assert not Path("proj/tests/extra.file").exists()
    assert not Path("proj/tests/another.file").exists()

    # and an extension with extra files,
    def add_files(struct, opts):
        struct = structure.ensure(struct, "tests/extra.file", "content")
        struct = structure.merge(struct, {"tests": {"another.file": "content"}})

        return struct, opts

    # when the created project is called,
    create_project(project_path="proj", extensions=[create_extension(add_files)])

    # then the files should be created
    assert Path("proj/tests/extra.file").exists()
    assert tmpfolder.join("proj/tests/extra.file").read() == "content"
    assert Path("proj/tests/another.file").exists()
    assert tmpfolder.join("proj/tests/another.file").read() == "content"


def test_create_project_respect_operations(tmpfolder, git_mock):
    # Given an existing project
    create_project(project_path="proj")
    for i in (0, 1, 3, 5, 6):
        tmpfolder.ensure("proj/tests/file" + str(i)).write("old")
        assert Path("proj/tests/file" + str(i)).exists()

    # and an extension with extra files
    def add_files(struct, opts):
        nov, sou = operations.no_overwrite(), operations.skip_on_update()
        struct = structure.ensure(struct, "tests/file0", "new")
        struct = structure.ensure(struct, "tests/file1", "new", nov)
        struct = structure.ensure(struct, "tests/file2", "new", sou)
        struct = structure.merge(
            struct,
            {
                "tests": {
                    "file3": ("new", nov),
                    "file4": ("new", sou),
                    "file5": ("new", operations.create),
                    "file6": "new",
                }
            },
        )

        return struct, opts

    # When the created project is called,
    create_project(
        project_path="proj", update=True, extensions=[create_extension(add_files)]
    )

    # then the NO_CREATE files should not be created,
    assert not Path("proj/tests/file2").exists()
    assert not Path("proj/tests/file4").exists()
    # the NO_OVERWRITE files should not be updated
    assert tmpfolder.join("proj/tests/file1").read() == "old"
    assert tmpfolder.join("proj/tests/file3").read() == "old"
    # and files with no rules or `None` rules should be updated
    assert tmpfolder.join("proj/tests/file0").read() == "new"
    assert tmpfolder.join("proj/tests/file5").read() == "new"
    assert tmpfolder.join("proj/tests/file6").read() == "new"


def test_create_project_when_folder_exists(tmpfolder, git_mock):
    tmpfolder.ensure("my-project", dir=True)
    opts = dict(project_path="my-project")
    with pytest.raises(DirectoryAlreadyExists):
        create_project(opts)
    opts = dict(project_path="my-project", force=True)
    create_project(opts)


def test_create_project_with_valid_package_name(tmpfolder, git_mock):
    opts = dict(project_path="my-project", package="my_package")
    create_project(opts)


def test_create_project_with_invalid_package_name(tmpfolder, git_mock):
    opts = dict(project_path="my-project", package="my:package")
    with pytest.raises(InvalidIdentifier):
        create_project(opts)


def test_create_project_when_updating(tmpfolder, git_mock):
    opts = dict(project_path="my-project")
    create_project(opts)
    opts = dict(project_path="my-project", update=True)
    create_project(opts)
    assert Path("my-project").exists()