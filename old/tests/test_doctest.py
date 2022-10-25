import doctest

import old.freegames.utils


def test_utils():
    failures, _ = doctest.testmod(old.freegames.utils)
    assert failures == 0
