from dataclasses import dataclass, fields


@dataclass
class Person:
    lastname: str
    firstname: str
    surname: str
    organization: str
    position: str
    phone: str
    email: str

    def get_value(self, key):
        return self.__getattribute__(key)

    def set_value(self, key, value):
        return self.__setattr__(key, value)

    def __iter__(self):
        return iter(self.__class__.get_fields_names())

    def dict_view(self):
        person = dict()
        for key in self:
            person[key] = self.get_value(key)
        return person

    @classmethod
    def get_fields_names(cls):
        return list(i.name for i in fields(cls))
