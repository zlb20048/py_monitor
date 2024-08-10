import os


class KeyValueStore:
    def __init__(self, filename):
        self.filename = filename
        if not os.path.exists(filename):
            with open(filename, 'w') as file:
                pass

    def _read_file(self):
        data = {}
        with open(self.filename, 'r') as file:
            for line in file:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    data[key] = value
        return data

    def _write_file(self, data):
        with open(self.filename, 'w') as file:
            for key, value in data.items():
                file.write(f"{key}={value}\n")

    def add(self, key, value):
        data = self._read_file()
        data[key] = value
        self._write_file(data)

    def update(self, key, value):
        data = self._read_file()
        if key in data:
            data[key] = value
            self._write_file(data)
        else:
            print(f"Key '{key}' does not exist.")

    def delete(self, key):
        data = self._read_file()
        if key in data:
            del data[key]
            self._write_file(data)
        else:
            print(f"Key '{key}' does not exist.")

    def get(self, key):
        data = self._read_file()
        return data.get(key, f"Key '{key}' not found.")

    def list_all(self):
        data = self._read_file()
        for key, value in data.items():
            print(f"{key}={value}")
