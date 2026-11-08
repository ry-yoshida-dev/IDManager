from dataclasses import dataclass, field
from threading import Lock


@dataclass
class IDManager:
    """
    Issue sequential integer IDs in a thread-safe manner.

    Parameters
    ----------
    current_id : int, optional
        The ID that the next call to `next_id` returns. Default is 0.
    step : int, optional
        The increment between consecutive IDs. May be negative. Default is 1.

    Raises
    ------
    ValueError
        If `step` is 0.
    """

    current_id: int = 0
    step: int = 1
    _lock: Lock = field(default_factory=Lock, init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self.step == 0:
            raise ValueError("step must not be 0")

    def next_id(self) -> int:
        """
        Return the current ID and advance it by `step`.

        Returns
        -------
        int
            The issued ID.
        """
        with self._lock:
            issued_id: int = self.current_id
            self.current_id += self.step
            return issued_id

    def reset(self, start: int = 0) -> None:
        """
        Restart the sequence so that the next issued ID is `start`.

        Parameters
        ----------
        start : int, optional
            The next ID to issue. Default is 0.
        """
        with self._lock:
            self.current_id = start
