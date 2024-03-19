from typing import List, Optional, Union

import numpy as np
import pandas as pd
from scipy.sparse import csr_array

from skfp.fingerprints.base import FingerprintTransformer


class SECFPFingerprint(FingerprintTransformer):
    def __init__(
        self,
        fp_size: int = 2048,
        radius: int = 3,
        min_radius: int = 1,
        rings: bool = True,
        isomeric: bool = False,
        kekulize: bool = True,
        sparse: bool = False,
        n_jobs: Optional[int] = None,
        verbose: int = 0,
    ):
        super().__init__(
            sparse=sparse,
            n_jobs=n_jobs,
            verbose=verbose,
        )
        self.fp_size = fp_size
        self.radius = radius
        self.min_radius = min_radius
        self.rings = rings
        self.isomeric = isomeric
        self.kekulize = kekulize

    def _calculate_fingerprint(
        self, X: Union[pd.DataFrame, np.ndarray, List[str]]
    ) -> Union[np.ndarray, csr_array]:
        from rdkit.Chem.rdMHFPFingerprint import MHFPEncoder

        X = self._validate_input(X)

        # bulk function does not work
        encoder = MHFPEncoder(self.fp_size, self.random_state)
        X = [
            encoder.EncodeSECFPMol(
                x,
                length=self.fp_size,
                radius=self.radius,
                min_radius=self.min_radius,
                rings=self.rings,
                isomeric=self.isomeric,
                kekulize=self.kekulize,
            )
            for x in X
        ]

        return csr_array(X) if self.sparse else np.array(X)
