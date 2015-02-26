import pytest
from kuhn3p import betting

def test_to_string():
    assert betting.num_internal() == 12
    assert betting.num_terminals() == 13
    for state in range(betting.num_internal(), betting.num_internal() + betting.num_terminals()):
        assert betting.string_to_state(betting.to_string(state)) == state


