import numpy as np
from rdkit.Chem.rdFingerprintGenerator import GetMorganGenerator
from scipy.sparse import csr_array

from skfp.fingerprints import ECFPFingerprint


def test_ecfp_bit_fingerprint(smiles_list, mols_list):
    ecfp_fp = ECFPFingerprint(sparse=False, count=False, n_jobs=-1)
    X_skfp = ecfp_fp.transform(smiles_list)

    fp_gen = GetMorganGenerator()
    X_rdkit = np.array([fp_gen.GetFingerprintAsNumPy(mol) for mol in mols_list])

    assert np.array_equal(X_skfp, X_rdkit)


def test_ecfp_count_fingerprint(smiles_list, mols_list):
    ecfp_fp = ECFPFingerprint(sparse=False, count=True, n_jobs=-1)
    X_skfp = ecfp_fp.transform(smiles_list)

    fp_gen = GetMorganGenerator()
    X_rdkit = np.array([fp_gen.GetCountFingerprintAsNumPy(mol) for mol in mols_list])

    assert np.array_equal(X_skfp, X_rdkit)


def test_ecfp_sparse_bit_fingerprint(smiles_list, mols_list):
    ecfp_fp = ECFPFingerprint(sparse=True, count=False, n_jobs=-1)
    X_skfp = ecfp_fp.transform(smiles_list)

    fp_gen = GetMorganGenerator()
    X_rdkit = csr_array([fp_gen.GetFingerprintAsNumPy(mol) for mol in mols_list])

    assert np.array_equal(X_skfp.data, X_rdkit.data)


def test_ecfp_sparse_count_fingerprint(smiles_list, mols_list):
    ecfp_fp = ECFPFingerprint(sparse=True, count=True, n_jobs=-1)
    X_skfp = ecfp_fp.transform(smiles_list)

    fp_gen = GetMorganGenerator()
    X_rdkit = csr_array([fp_gen.GetCountFingerprintAsNumPy(mol) for mol in mols_list])

    assert np.array_equal(X_skfp.data, X_rdkit.data)
