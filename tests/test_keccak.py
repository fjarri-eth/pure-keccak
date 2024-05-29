import os

import pytest
from Crypto.Hash import keccak as pycryptodome_keccak

from pure_keccak import Keccak224, Keccak256, Keccak384, Keccak512


def keccak_ref(bits, s):
    keccak_hash = pycryptodome_keccak.new(digest_bits=bits)
    keccak_hash.update(s)
    return keccak_hash.digest()


def keccak(bits, s):
    cls = {
        224: Keccak224,
        256: Keccak256,
        384: Keccak384,
        512: Keccak512,
    }

    return cls[bits]().update(s).digest()


def run_keccak(s):
    return Keccak256().update(s).digest()


def test_performance(benchmark):
    s = os.urandom(128)
    test = benchmark(run_keccak, s)

    ref = keccak_ref(256, s)
    assert test == ref


@pytest.mark.parametrize("bits", [224, 256, 384, 512])
def test_correctness(bits):
    assert keccak_ref(bits, b"") == keccak(bits, b"")
    for size in (1, 10, 16, 25, 32, 50, 64, 100, 128, 200, 256):
        for i in range(100):
            s = os.urandom(size)
            assert keccak_ref(bits, s) == keccak(bits, s)
