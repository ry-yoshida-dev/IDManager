from concurrent.futures import ThreadPoolExecutor

import pytest

from id_manager import IDManager


def test_initialization_uses_defaults() -> None:
    manager: IDManager = IDManager()
    assert manager.current_id == 0
    assert manager.step == 1


def test_initialization_accepts_custom_values() -> None:
    manager: IDManager = IDManager(current_id=10, step=2)
    assert manager.current_id == 10
    assert manager.step == 2


def test_initialization_rejects_zero_step() -> None:
    with pytest.raises(ValueError):
        _ = IDManager(step=0)


def test_next_id_returns_current_and_advances() -> None:
    manager: IDManager = IDManager(current_id=5, step=3)
    assert manager.next_id() == 5
    assert manager.current_id == 8
    assert manager.next_id() == 8
    assert manager.current_id == 11


def test_next_id_supports_negative_step() -> None:
    manager: IDManager = IDManager(current_id=0, step=-1)
    assert [manager.next_id() for _ in range(3)] == [0, -1, -2]


def test_reset_restarts_sequence() -> None:
    manager: IDManager = IDManager(current_id=10, step=2)
    _ = manager.next_id()
    manager.reset()
    assert manager.next_id() == 0

    manager.reset(start=100)
    assert manager.next_id() == 100


def test_next_id_is_unique_across_threads() -> None:
    manager: IDManager = IDManager()
    count: int = 10_000

    def issue(_: int) -> int:
        return manager.next_id()

    with ThreadPoolExecutor(max_workers=8) as executor:
        issued_ids: list[int] = list(executor.map(issue, range(count)))
    assert sorted(issued_ids) == list(range(count))


def test_repr_and_equality_ignore_lock() -> None:
    manager: IDManager = IDManager(current_id=10, step=2)
    assert repr(manager) == "IDManager(current_id=10, step=2)"
    assert manager == IDManager(current_id=10, step=2)
