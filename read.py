import struct


class Reader:
    def __init__(self, data):
        self.data = data
        self.offset = 0

    def uint8(self):
        value = struct.unpack_from('<B', self.data, self.offset)[0]
        self.offset += 1
        return value

    def uint16(self):
        value = struct.unpack_from('<H', self.data, self.offset)[0]
        self.offset += 2
        return value

    def uint32(self):
        value = struct.unpack_from('<I', self.data, self.offset)[0]
        self.offset += 4
        return value

    def int32(self):
        value = struct.unpack_from('<i', self.data, self.offset)[0]
        self.offset += 4
        return value

    def uint64(self):
        value = struct.unpack_from('<Q', self.data, self.offset)[0]
        self.offset += 8
        return value

    def float32(self):
        value = struct.unpack_from('<f', self.data, self.offset)[0]
        self.offset += 4
        return value

    def vec3(self):
        value = struct.unpack_from('<3f', self.data, self.offset)
        self.offset += 12
        return value

    def vec4(self):
        value = struct.unpack_from('<4f', self.data, self.offset)
        self.offset += 16
        return value

    def matrix3x4(self):
        value = struct.unpack_from('<12f', self.data, self.offset)
        self.offset += 48
        return value

    def matrix4x4(self):
        value = struct.unpack_from('<16f', self.data, self.offset)
        self.offset += 64
        return value

    def string(self):
        byte = None
        zero_pos = self.offset

        while byte != 0:
            byte = self.data[zero_pos]
            zero_pos += 1

        string_size = zero_pos - self.offset - 1
        string = struct.unpack_from('<{}s'.format(string_size), self.data, self.offset)[0].decode(encoding='cp1251')
        self.offset = zero_pos

        return string

    def skip(self, size):
        self.offset += size

    def get_bytes(self, size):
        data = self.data[self.offset : self.offset + size]
        self.offset += size
        return data


class Chunks:
    def __init__(self, data):
        self.data = data
        self.size = len(data)
        self._offset = 0
        self._current_chunk = 0
        self._chunks_count = 0

        self.chunks = []

        self._read()

    def _read_chunk(self):
        chunk_id, chunk_size = struct.unpack_from('<2I', self.data, self._offset)
        self._offset += 8

        chunk_data = self.data[self._offset : self._offset + chunk_size]
        self._offset += chunk_size

        self.chunks.append((chunk_id, chunk_data))

    def _read(self):
        while self._offset < self.size:
            self._read_chunk()

        self._chunks_count = len(self.chunks)

    def __next__(self):
        if self._current_chunk >= self._chunks_count:
            self._current_chunk = 0
            raise StopIteration

        chunk_id, chunk_data = self.chunks[self._current_chunk]
        self._current_chunk += 1

        return chunk_id, chunk_data

    def __iter__(self):
        return self
