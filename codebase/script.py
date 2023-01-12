
from unittest import mock

_stdin = [45]


def mock_input(var1):
    return _stdin.pop(0)


input = mock.Mock(side_effect=mock_input)
print("Hellooo my friend")