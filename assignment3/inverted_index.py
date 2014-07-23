import MapReduce
import sys

__author__ = 'mhotan'

# Import the library
mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
    key = record[0]
    value = record[1]
    words = value.split()
    for w in words:
        mr.emit_intermediate(w.strip().encode('utf-8'), key.encode('utf-8'))

def reducer(key, list_of_values):
    # key: word
    # value: list of appearing documents
    print (key, list(set(list_of_values)))
    mr.emit((key, list(set(list_of_values))))

# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)