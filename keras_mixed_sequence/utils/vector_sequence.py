"""Module offering object to handle Vector Keras Sequences."""
import numpy as np
from .sequence import Sequence


class VectorSequence(Sequence):
    """Wrapper of Keras Sequence to handle some commonly used methods and properties."""

    def __init__(
        self,
        vector: np.ndarray,
        batch_size: int,
        seed: int = 42,
        elapsed_epochs: int = 0
    ):
        """Return new Sequence object.

        Parameters
        -------------------------------------
        vector: np.ndarray,
            Numpy array with data to be split into batches.
        batch_size: int,
            Batch size for the current Sequence.
        seed: int = 42,
            Random seed to use for reproducibility.
        elapsed_epochs: int = 0,
            Number of elapsed epochs to init state of generator.

        Returns
        -------------------------------------
        Return new Sequence object.
        """
        super().__init__(
            len(vector),
            batch_size,
            elapsed_epochs
        )
        self._seed = seed
        self._vector = vector
        self._shuffled = vector.copy()

    def on_epoch_end(self):
        """Shuffle private numpy array on every epoch end."""
        super().on_epoch_end()
        state = np.random.RandomState(  # pylint: disable=no-member
            seed=self._seed + self._elapsed_epochs
        )
        indices = np.arange(self.samples_number)
        state.shuffle(indices)
        self._shuffled = self._vector[indices]

    def __getitem__(self, idx: int) -> np.ndarray:
        """Return batch corresponding to given index.

        Parameters
        ---------------------
        idx: int,
            Index corresponding to batch to be rendered.

        Returns
        ---------------------
        Return numpy array corresponding to given batch index.
        """
        if idx >= self.steps_per_epoch:
            raise ValueError(
                (
                    "Given index {idx} is greater than the number "
                    "of steps per epoch of this sequence {steps}."
                ).format(
                    idx=idx,
                    steps=self.steps_per_epoch
                )
            )
        return self._shuffled[idx * self.batch_size: (idx + 1) * self.batch_size]
