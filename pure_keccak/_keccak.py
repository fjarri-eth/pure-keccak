from collections.abc import Callable
from math import log

# The Keccak-f round constants.
ROUND_CONSTANTS = [
    0x0000000000000001,
    0x0000000000008082,
    0x800000000000808A,
    0x8000000080008000,
    0x000000000000808B,
    0x0000000080000001,
    0x8000000080008081,
    0x8000000000008009,
    0x000000000000008A,
    0x0000000000000088,
    0x0000000080008009,
    0x000000008000000A,
    0x000000008000808B,
    0x800000000000008B,
    0x8000000000008089,
    0x8000000000008003,
    0x8000000000008002,
    0x8000000000000080,
    0x000000000000800A,
    0x800000008000000A,
    0x8000000080008081,
    0x8000000000008080,
    0x0000000080000001,
    0x8000000080008008,
]

ROT_01 = 36
ROT_02 = 3
ROT_03 = 41
ROT_04 = 18
ROT_05 = 1
ROT_06 = 44
ROT_07 = 10
ROT_08 = 45
ROT_09 = 2
ROT_10 = 62
ROT_11 = 6
ROT_12 = 43
ROT_13 = 15
ROT_14 = 61
ROT_15 = 28
ROT_16 = 55
ROT_17 = 25
ROT_18 = 21
ROT_19 = 56
ROT_20 = 27
ROT_21 = 20
ROT_22 = 39
ROT_23 = 8
ROT_24 = 14


MASKS = [(1 << i) - 1 for i in range(65)]


def bits2bytes(x: int) -> int:
    return (x + 7) // 8


def rol(value: int, left: int, bits: int) -> int:
    """
    Circularly rotate 'value' to the left,
    treating it as a quantity of the given size in bits.
    """
    top = value >> (bits - left)
    bot = (value & MASKS[bits - left]) << left
    return bot | top


def keccak_function(state: list[int], lane_width: int) -> None:
    rounds = 12 + 2 * int(log(lane_width, 2))

    a0 = state[0]
    a1 = state[1]
    a2 = state[2]
    a3 = state[3]
    a4 = state[4]
    a5 = state[5]
    a6 = state[6]
    a7 = state[7]
    a8 = state[8]
    a9 = state[9]
    a10 = state[10]
    a11 = state[11]
    a12 = state[12]
    a13 = state[13]
    a14 = state[14]
    a15 = state[15]
    a16 = state[16]
    a17 = state[17]
    a18 = state[18]
    a19 = state[19]
    a20 = state[20]
    a21 = state[21]
    a22 = state[22]
    a23 = state[23]
    a24 = state[24]

    for i in range(rounds):
        # Prepare column parity for Theta step
        c0 = a0 ^ a5 ^ a10 ^ a15 ^ a20
        c1 = a1 ^ a6 ^ a11 ^ a16 ^ a21
        c2 = a2 ^ a7 ^ a12 ^ a17 ^ a22
        c3 = a3 ^ a8 ^ a13 ^ a18 ^ a23
        c4 = a4 ^ a9 ^ a14 ^ a19 ^ a24

        # Theta + Rho + Pi steps
        d = c4 ^ rol(c1, 1, lane_width)
        b0 = d ^ a0
        b16 = rol(d ^ a5, ROT_01, lane_width)
        b7 = rol(d ^ a10, ROT_02, lane_width)
        b23 = rol(d ^ a15, ROT_03, lane_width)
        b14 = rol(d ^ a20, ROT_04, lane_width)

        d = c0 ^ rol(c2, 1, lane_width)
        b10 = rol(d ^ a1, ROT_05, lane_width)
        b1 = rol(d ^ a6, ROT_06, lane_width)
        b17 = rol(d ^ a11, ROT_07, lane_width)
        b8 = rol(d ^ a16, ROT_08, lane_width)
        b24 = rol(d ^ a21, ROT_09, lane_width)

        d = c1 ^ rol(c3, 1, lane_width)
        b20 = rol(d ^ a2, ROT_10, lane_width)
        b11 = rol(d ^ a7, ROT_11, lane_width)
        b2 = rol(d ^ a12, ROT_12, lane_width)
        b18 = rol(d ^ a17, ROT_13, lane_width)
        b9 = rol(d ^ a22, ROT_14, lane_width)

        d = c2 ^ rol(c4, 1, lane_width)
        b5 = rol(d ^ a3, ROT_15, lane_width)
        b21 = rol(d ^ a8, ROT_16, lane_width)
        b12 = rol(d ^ a13, ROT_17, lane_width)
        b3 = rol(d ^ a18, ROT_18, lane_width)
        b19 = rol(d ^ a23, ROT_19, lane_width)

        d = c3 ^ rol(c0, 1, lane_width)
        b15 = rol(d ^ a4, ROT_20, lane_width)
        b6 = rol(d ^ a9, ROT_21, lane_width)
        b22 = rol(d ^ a14, ROT_22, lane_width)
        b13 = rol(d ^ a19, ROT_23, lane_width)
        b4 = rol(d ^ a24, ROT_24, lane_width)

        # Chi + Iota steps
        a0 = b0 ^ (~b1 & b2) ^ ROUND_CONSTANTS[i]
        a1 = b1 ^ (~b2 & b3)
        a2 = b2 ^ (~b3 & b4)
        a3 = b3 ^ (~b4 & b0)
        a4 = b4 ^ (~b0 & b1)

        a5 = b5 ^ (~b6 & b7)
        a6 = b6 ^ (~b7 & b8)
        a7 = b7 ^ (~b8 & b9)
        a8 = b8 ^ (~b9 & b5)
        a9 = b9 ^ (~b5 & b6)

        a10 = b10 ^ (~b11 & b12)
        a11 = b11 ^ (~b12 & b13)
        a12 = b12 ^ (~b13 & b14)
        a13 = b13 ^ (~b14 & b10)
        a14 = b14 ^ (~b10 & b11)

        a15 = b15 ^ (~b16 & b17)
        a16 = b16 ^ (~b17 & b18)
        a17 = b17 ^ (~b18 & b19)
        a18 = b18 ^ (~b19 & b15)
        a19 = b19 ^ (~b15 & b16)

        a20 = b20 ^ (~b21 & b22)
        a21 = b21 ^ (~b22 & b23)
        a22 = b22 ^ (~b23 & b24)
        a23 = b23 ^ (~b24 & b20)
        a24 = b24 ^ (~b20 & b21)

    state[0] = a0
    state[1] = a1
    state[2] = a2
    state[3] = a3
    state[4] = a4
    state[5] = a5
    state[6] = a6
    state[7] = a7
    state[8] = a8
    state[9] = a9
    state[10] = a10
    state[11] = a11
    state[12] = a12
    state[13] = a13
    state[14] = a14
    state[15] = a15
    state[16] = a16
    state[17] = a17
    state[18] = a18
    state[19] = a19
    state[20] = a20
    state[21] = a21
    state[22] = a22
    state[23] = a23
    state[24] = a24


class KeccakState:
    """
    A keccak state container.

    The state is stored as a 5x5 table of integers.
    """

    @staticmethod
    def lane2bytes(s: int, w: int) -> list[int]:
        """
        Converts the lane s to a sequence of byte values,
        assuming a lane is w bits.
        """
        o = []
        for b in range(0, w, 8):
            o.append((s >> b) & 0xFF)
        return o

    @staticmethod
    def bytes2lane(data: list[int]) -> int:
        """
        Converts a sequence of byte values to a lane.
        """
        r = 0
        for b in reversed(data):
            r = r << 8 | b
        return r

    def __init__(self, byterate: int, lane_width: int):
        self.byterate = byterate
        self.lane_width = lane_width
        self.s = [0] * 25

    def absorb(self, data: list[int]) -> None:
        """
        Mixes in the given bitrate-length string to the state.
        """
        assert len(data) == self.byterate

        data += [0] * bits2bytes(self.lane_width * 25 - self.byterate * 8)
        i = 0

        # TODO: should the array length given to `bytes2lane()` be `lane_width // 8`
        # instead of hardcoded 8?
        for i in range(25):
            self.s[i] ^= self.bytes2lane(data[i * 8 : i * 8 + 8])

    def squeeze(self) -> list[int]:
        """
        Returns the bitrate-length prefix of the state to be output.
        """
        return self.get_bytes()[: self.byterate]

    def get_bytes(self) -> list[int]:
        """
        Convert whole state to a byte string.
        """
        out = [0] * bits2bytes(self.lane_width * 25)

        for i in range(25):
            v = self.lane2bytes(self.s[i], self.lane_width)
            out[i * 8 : i * 8 + 8] = v

        return out


def multirate_padding(used_bytes: int, align_bytes: int) -> list[int]:
    """
    The Keccak padding function.
    """
    padlen = align_bytes - used_bytes
    if padlen == 0:
        padlen = align_bytes
    # note: padding done in 'internal bit ordering', wherein LSB is leftmost
    if padlen == 1:
        return [0x81]
    else:
        return [0x01] + ([0x00] * (padlen - 2)) + [0x80]


class KeccakSponge:
    def __init__(self, byterate: int, lane_width: int):
        self._state = KeccakState(byterate, lane_width)
        self._buffer: list[int] = []

    def _absorb_block(self, data: list[int]) -> None:
        assert len(data) == self._state.byterate
        self._state.absorb(data)
        keccak_function(self._state.s, self._state.lane_width)

    def absorb(self, data: bytes) -> None:
        self._buffer += list(data)

        while len(self._buffer) >= self._state.byterate:
            self._absorb_block(self._buffer[: self._state.byterate])
            self._buffer = self._buffer[self._state.byterate :]

    def absorb_final(self) -> None:
        padded = self._buffer + multirate_padding(len(self._buffer), self._state.byterate)
        self._absorb_block(padded)
        self._buffer = []

    def _squeeze_once(self) -> list[int]:
        rc = self._state.squeeze()
        keccak_function(self._state.s, self._state.lane_width)
        return rc

    def squeeze(self, size: int) -> bytes:
        Z = self._squeeze_once()
        while len(Z) < size:
            Z += self._squeeze_once()
        return bytes(Z[:size])


class KeccakHash:
    """
    The Keccak hash function, with a hashlib-compatible interface.
    """

    def __init__(self, bitrate: int, capacity_bits: int, output_bits: int):
        assert bitrate + capacity_bits in (25, 50, 100, 200, 400, 800, 1600)
        assert output_bits % 8 == 0
        assert bitrate % 8 == 0

        self._sponge = KeccakSponge(bitrate // 8, (bitrate + capacity_bits) // 25)
        self._digest_size = output_bits // 8

    def update(self, data: bytes) -> "KeccakHash":
        self._sponge.absorb(data)
        return self

    def digest(self) -> bytes:
        # Note: this invalidates the object
        self._sponge.absorb_final()
        return self._sponge.squeeze(self._digest_size)

    @classmethod
    def preset(
        cls, bitrate: int, capacity_bits: int, output_bits: int
    ) -> Callable[[], "KeccakHash"]:
        """
        Returns a factory function for the given bitrate, sponge capacity and output length.
        The function accepts an optional initial input, ala hashlib.
        """

        def create() -> "KeccakHash":
            return cls(bitrate, capacity_bits, output_bits)

        return create


# SHA3 parameter presets
Keccak224 = KeccakHash.preset(1152, 448, 224)
Keccak256 = KeccakHash.preset(1088, 512, 256)
Keccak384 = KeccakHash.preset(832, 768, 384)
Keccak512 = KeccakHash.preset(576, 1024, 512)
