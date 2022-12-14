class WaveHead:
    def __init__(self, filename):
        try:
            if not filename.endswith('wav'):
                raise RuntimeError

            with open(filename, 'rb') as file:
                self.data = file.read()

                if len(self.data) < 44:
                    raise RuntimeError

                self.file_size = self.little_endian_convert(self.data[4:8])
                self.format_type = self.little_endian_convert(self.data[20:22])
                self.nchannels = self.little_endian_convert(self.data[22:24])
                self.framerate = self.little_endian_convert(self.data[24:28])
                self.bps = self.little_endian_convert(self.data[34:36])
                self.data_size = self.little_endian_convert(self.data[40:44])

                print(self)
        except Exception:
            print("NO")

    def __str__(self):
        return f"Size={self.file_size}, Type={self.format_type}, Channels={self.nchannels}, Rate={self.framerate}, Bits={self.bps}, Data size={self.data_size}"

    @staticmethod
    def little_endian_convert(byte_arr):
        res = 0
        for i in range(len(byte_arr) - 1, -1, -1):
            res += byte_arr[i]
            res = res << 8
        return res >> 8


if __name__ == '__main__':
    filepath = input()
    WaveHead(filepath)
