from classes.parser import Parser
from classes.csv_file import CsvPersonFile


def run():
    parser = Parser()
    parser.parse('phone_raw.csv')
    csv_file = CsvPersonFile(parser.people)
    csv_file.create_file('new_persons.csv')


if __name__ == '__main__':
    run()
