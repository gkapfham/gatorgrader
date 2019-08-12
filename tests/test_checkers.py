"""Tests for the loading, verification, and use of plugin-based checkers."""


from gator import arguments
from gator import checkers


def test_checkerdir_extraction_from_commandline_arguments(tmpdir):
    """Check that command-line argument extraction works in checker function."""
    _ = tmpdir.mkdir("checks").join("check_messages.py")
    assert len(tmpdir.listdir()) == 1
    checker_directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "checks"
    commandline_arguments = ["--checkerdir", checker_directory, "check_messages"]
    gg_arguments = arguments.parse(commandline_arguments)
    args_verified = arguments.verify(gg_arguments)
    assert args_verified is True
    found_checker_directory = checkers.get_checker_dir(gg_arguments)
    assert found_checker_directory == checker_directory


def test_load_checkers_list_is_not_empty_default_input():
    """Ensures checker loading results in non-empty list with defaults."""
    checker_source = checkers.get_source()
    # the source for the plugins is not empty
    assert checker_source is not None
    # the source for the plugins contains plugins
    # that adhere to the naming scheme "check_<ACTION>"
    # for instance "check_commits"
    # we know that this should be true because all
    # internal GatorGrader plugins adhere to this convention
    for checker in checker_source.list_plugins():
        assert "check_" in checker


def test_load_checkers_list_is_not_empty_provided_input(tmpdir):
    """Ensures checker loading results in non-empty list with provided list."""
    # create a single checker in a new directory
    checker_file = tmpdir.mkdir("internal_checkers").join("check_testing.py")
    checker_file.write("a checker")
    checker_directory = (
        tmpdir.dirname + "/" + tmpdir.basename + "/" + "internal_checkers"
    )
    list_of_checker_directories = [checker_directory]
    checker_source = checkers.get_source(list_of_checker_directories)
    assert checker_source is not None
    checker_source_list = checker_source.list_plugins()
    assert len(checker_source_list) >= 1