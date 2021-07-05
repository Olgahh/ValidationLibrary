import sys
from validationlib.validator import Validator

if __name__ == '__main__':
    file = sys.argv
    file = "".join(file[1])
    a = Validator(file)
    a.check_file()