import json


class CustomProperty:
    def __init__(self, getter):
        self.getter = getter
        self._setter = None
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.getter(instance)

    def __set__(self, instance, value):
        if self._setter is not None:
            self._setter(instance, value)
        else:
            raise AttributeError("Cannot set value directly. Use the setter method.")

    def setter(self, setter):
        self._setter = setter
        return self


class PersistentClass:
    def __init__(self, file_name):
        self._file_path = f"{file_name}.json"
        self._data = self._load_from_file()  # Initialize with data from file or an empty dictionary if file not found

    @CustomProperty
    def data(self):
        return self._data

    def add_value(self, key, value):
        self._data[key] = value
        self._save_to_file()

    def update_value(self, key, new_value):
        if key in self._data:
            self._data[key] = new_value
            self._save_to_file()
        else:
            raise KeyError(f"Key '{key}' not found in data.")

    def _load_from_file(self):
        try:
            with open(self._file_path, 'r') as file:
                data = json.load(file)
                return data.get('data', {})
        except FileNotFoundError:
            return {}

    def _save_to_file(self):
        data = {'data': self._data}
        with open(self._file_path, 'w') as file:
            json.dump(data, file)
