import sys
import MapReduce

__author__ = 'mhotan'

"""
Executes the same query as a SQL Join
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: Equal ID
    # value: Record that the id is in.
    string_record = []
    for attr in record:
        string_record.append(attr.encode('utf-8'))

    mr.emit_intermediate(string_record[1], string_record)


def is_order(record):
    return record[0] == 'order'


def is_line_item(record):
    return record[0] == 'line_item'


def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    for order in filter(is_order, list_of_values):
        for line_item in filter(is_line_item, list_of_values):
            print order + line_item
            mr.emit(order + line_item)

# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)