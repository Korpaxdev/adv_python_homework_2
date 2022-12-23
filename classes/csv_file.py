from csv import DictWriter

from classes.person import Person


class CsvPersonFile:

    def __init__(self, people: list[Person]):
        self.__people = people

    def create_file(self, file_name: str):
        fields = self.__get_fields()
        with open(file_name, 'w+', encoding='utf-8') as file:
            reader = DictWriter(file, fieldnames=fields)
            reader.writeheader()
            self.__write_rows(reader)

    @staticmethod
    def __get_fields() -> list:
        return Person.get_fields_names()

    def __write_rows(self, reader: DictWriter):
        for person in self.__people:
            reader.writerow(person.dict_view())
