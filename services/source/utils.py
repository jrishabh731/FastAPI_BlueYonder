import csv
from io import StringIO


class Utils:
    @classmethod
    def csv_to_dict(cls, bytes_stream, delimiter=",", encoding='utf-8-sig'):
        return csv.DictReader(StringIO(str(bytes_stream, encoding)), delimiter=delimiter)


