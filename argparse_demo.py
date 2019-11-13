import argparse
import sys

program_epilog = """
This is some huge block of text\n
with multiple lines in it."""

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    if len(sys.argv) == 1:
        parser.print_help()
        print(program_epilog)
    else:

        parser.add_argument('demo', metavar='d', type=int, nargs=2, 
                        help='This tells you what to do')

        args = parser.parse_args()