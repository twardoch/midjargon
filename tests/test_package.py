# this_file: tests/test_package.py
"""Test suite for midjargon."""


def test_version():
    """Verify package exposes version."""
    import midjargon

    assert midjargon.__version__
