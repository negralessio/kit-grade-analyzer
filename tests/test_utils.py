# Executed via python -m pytest -v --cov tests/ from root
import pytest

import src.utils as utils
import src.constants as constants


@pytest.mark.parametrize(
    "x, sep, expected",
    [
        ("", constants.SEP, [""]),
        ("URL1", constants.SEP, ["URL1"]),
        ("URL1$URL2", constants.SEP, ["URL1", "URL2"]),
        ("URL1$URL2$URL3", constants.SEP, ["URL1", "URL2", "URL3"]),
        ("URL1$$$$URL2", constants.SEP, ["URL1", "", "", "", "URL2"])
    ]
)
def test_separate_input_string_return_correct_list(x: str, sep: str, expected: list[str]):
    assert utils.separate_input_string(x, sep) == expected


def test_separate_input_string_separator_token_empty_return_ValueError():
    with pytest.raises(ValueError):
        utils.separate_input_string("URL1$URL2", "")
