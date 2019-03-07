"""Retrieve and count the tags of a markdown file"""

from pathlib import Path

import commonmark

from gator import util

FILE_SEPARATOR = "/"


def count_specified_tag(contents, tag):
    """Counts the specified markdown tag in the string contents"""
    ast = commonmark.Parser().parse(contents)
    mode_looking = True
    tag_count = 0

    # TODO: implement counting algorithm
    for subnode, enter in ast.walker():
        if mode_looking:
            # Check to see if the current subnode is an open node of the specified tag
            if tag_count == 1 and subnode.t == tag and enter:
                # Stop search for nodes of the specified tag, as one has been found
                mode_looking = False
        else:
            # Check to see if the current subnode is a closing node for the specified tag
            if tag_count == 2 and subnode.t == tag and not enter:
                # Start a search for a new specified item
                mode_looking = True

        if subnode.is_container():
            if enter:
                tag_count += 1
            else:
                tag_count -= 1

    return tag_count


# pylint: disable=bad-continuation
def specified_tag_greater_than_count(
    chosen_tag,
    checking_function,
    expected_count,
    given_file,
    containing_directory,
    exact=False,
):
    """Determines if the tag count is greater than expected in a given file"""
    file_for_checking = Path(containing_directory + FILE_SEPARATOR + given_file)
    file_tag_count = 0
    if file_for_checking.is_file():
        file_contexts = file_for_checking.read_text()
        file_tag_count = checking_function(file_contents, chosen_tag)

    # check the condition and also return file_tag_count
    return util.greater_than_equal_exacted(file_tag_count, expected_count, exact)
