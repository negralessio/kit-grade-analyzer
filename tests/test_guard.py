import pytest

from src.guard import Guard


@pytest.mark.parametrize(
    "input_url, eval",
    [
        ("https://www.sle.kit.edu/dokumente", True),
        ("www.sle.kit.edu/dokumente", False),
        ("", False)
    ]
)
def test_check_input_return_true(input_url: str, eval: bool):
    # Arrange
    guard = Guard(input_url)
    # Act and Assert
    assert guard.check_input() == eval
