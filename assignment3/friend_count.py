import MapReduce
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # Record : Array where the first index is the person
    # The second element is the name of the friend
    mr.emit_intermediate(record[0], record[1])

def reducer(key, list_of_values):
    # key: Name of the person
    # value: All the occurences of their friend
    mr.emit((key, len(list_of_values)))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
