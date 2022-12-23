from csv import DictReader
from re import compile, Pattern

from classes.person import Person
from utils.patterns import MAIN_PHONE_PATTERN, ADD_PHONE_PATTERN


class Parser:
    def __init__(self):
        self.people: list[Person] | list = []
        self.__match_person: Person | None = None

    def parse(self, file_name: str):
        with open(file_name, encoding='utf-8') as file:
            data = list(DictReader(file))
            if not data:
                return None
            self.__set_people(data)

    def __set_people(self, data: list):
        for p in data:
            fullname = self.__get_fullname(p['lastname'], p['firstname'], p['surname'])
            last_name, first_name, surname = self.__get_split_names(fullname)
            phone = self.__get_valid_phone(p['phone'])
            person = Person(lastname=last_name, firstname=first_name, surname=surname, organization=p['organization'],
                            position=p['position'], phone=phone, email=p['email'])
            is_duplicate = self.__check_duplicates(person)
            if not is_duplicate:
                self.people.append(person)
            else:
                self.__check_empty_fields(person)

    @staticmethod
    def __get_fullname(lastname: str, firstname: str, surname: str) -> str:
        return " ".join((lastname, firstname, surname))

    def __check_duplicates(self, person: Person) -> bool:
        is_duplicate = False
        if self.people:
            for idx, p in enumerate(self.people):
                if p.lastname == person.lastname and p.firstname == person.firstname:
                    is_duplicate = True
                    self.__match_person = self.people[idx]
                    return is_duplicate
        return is_duplicate

    def __check_empty_fields(self, duplicate: Person):
        for key in self.__match_person:
            person_value = self.__match_person.get_value(key)
            duplicate_value = duplicate.get_value(key)
            if not person_value and duplicate_value:
                self.__match_person.set_value(key, duplicate_value)
            elif person_value and duplicate_value and person_value != duplicate_value:
                self.__match_person.set_value(key, person_value + duplicate_value)
        return False

    @staticmethod
    def __get_split_names(fullname: str) -> tuple[str, str, str | None]:
        names = fullname.split()
        last_name, first_name, *other = names
        surname = other[0] if other else None
        return last_name, first_name, surname

    def __get_valid_phone(self, phone_string: str) -> str | None:
        format_phone = ''
        add_format_phone = ''
        main_patter, add_pattern = self.__get_phone_patterns()
        main_search = main_patter.search(phone_string)
        if main_search and len(main_search.groups()) == 4:
            main_groups = main_search.groups()
            format_phone = f'+7({main_groups[0]}){main_groups[1]}-{main_groups[2]}-{main_groups[3]}'
        add_search = add_pattern.search(phone_string)
        if add_search:
            add_format_phone = f' доб.{add_search.group(1)}'
        return format_phone + add_format_phone

    @staticmethod
    def __get_phone_patterns() -> tuple[Pattern[str], Pattern[str]]:
        main_phone_pattern = compile(MAIN_PHONE_PATTERN)
        add_phone_pattern = compile(ADD_PHONE_PATTERN)
        return main_phone_pattern, add_phone_pattern
