import os
import sys

__author__ = 'mhotan'


def main():
    if len(sys.argv) != 2:
        raise ValueError('Incorrect argument signature\n Correct signature: '
                         'state_file_cleaner.py <state_file>')
    state_filepath = sys.argv[1]
    if not os.path.isfile(state_filepath):
        raise ValueError('Argument is not a file')
    state_file = open(state_filepath)

    try:
        os.remove('clean_state_file.txt')
    except OSError:
        pass
    output_file = open('clean_state_file.txt', mode='w')

    lines = state_file.readlines()
    print "Number of states present: " + str(len(lines))
    for state_line in lines:
        state_line = state_line.replace('name', '\'name\'')
        state_line = state_line.replace('code', '\'code\'')
        state_line = state_line.replace('borders', '\'borders\'')
        output_file.write(state_line)

    state_file.close()
    output_file.close()

if __name__ == '__main__':
    main()