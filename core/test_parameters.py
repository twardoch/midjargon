import pytest

from midjargon.core.parameters import parse_parameters


def test_invalid_parameters():
    """Test handling of invalid parameter formats."""
    with pytest.raises(SystemExit):
        parse_parameters("--")  # Empty parameter name

    with pytest.raises(SystemExit):
        parse_parameters("--ar")  # Missing required value

    with pytest.raises(SystemExit):
        parse_parameters("ar 16:9")  # Missing -- prefix

    with pytest.raises(SystemExit):
        parse_parameters("--v")  # Missing version value
