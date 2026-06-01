
from io import BytesIO, IOBase

class BinaryReader:
    def __init__(self, stream: IOBase, endian: str = '<', encoding: str = 'utf-8'):
        if not isinstance(stream, IOBase) or not hasattr(stream, 'read'):
            raise ValueError("Stream must be a file-like object with a read method.")
        self.stream = stream
        self.endian = endian
        self.encoding = encoding

    def _read_checked(self, size: int) -> bytes:
        data = self.stream.read(size)
        if len(data) < size:
            raise EOFError(f"Failed to read {size} bytes from stream.")
        return data

    def read_byte(self) -> int:
        data = self._read_checked(1)
        return data[0]

    def read_bytes(self, count: int) -> bytes:
        return self._read_checked(count)

    def read_bool(self) -> bool:
        data = self._read_checked(1)
        return data[0] != 0

    def read_int16(self) -> int:
        format_str = self.endian + 'h'
        data = self._read_checked(2)
        return struct.unpack(format_str, data)[0]

    def read_uint16(self) -> int:
        format_str = self.endian + 'H'
        data = self._read_checked(2)
        return struct.unpack(format_str, data)[0]

    def read_int32(self) -> int:
        format_str = self.endian + 'i'
        data = self._read_checked(4)
        return struct.unpack(format_str, data)[0]

    def read_uint32(self) -> int:
        format_str = self.endian + 'I'
        data = self._read_checked(4)
        return struct.unpack(format_str, data)[0]

    def read_int64(self) -> int:
        format_str = self.endian + 'q'
        data = self._read_checked(8)
        return struct.unpack(format_str, data)[0]

    def read_uint64(self) -> int:
        format_str = self.endian + 'Q'
        data = self._read_checked(8)
        return struct.unpack(format_str, data)[0]

    def read_single(self) -> float:
        format_str = self.endian + 'f'
        data = self._read_checked(4)
        return struct.unpack(format_str, data)[0]

    def read_double(self) -> float:
        format_str = self.endian + 'd'
        data = self._read_checked(8)
        return struct.unpack(format_str, data)[0]

    def read_string(self) -> str:
        length = self.read_7bit_encoded_int()
        if length < 0:
            raise ValueError("String length cannot be negative.")
        data = self._read_checked(length)
        return data.decode(self.encoding)

    def read_7bit_encoded_int(self) -> int:
        result = 0
        shift = 0
        while True:
            byte = self.read_byte()
            result |= (byte & 0x7F) << shift
            shift += 7
            if not (byte & 0x80):
                break
            if shift > 35:
                raise ValueError("Invalid 7-bit encoded integer format.")
        return result

