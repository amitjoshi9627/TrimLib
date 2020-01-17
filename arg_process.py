import argparse

def print_error(error_msg):
    if "unrecognized arguments" in error_msg:
        print("Invalid Arguments. Please see help [-h] or [--help]")
    else:
        pass

def parse_argument():
    parser = argparse.ArgumentParser(
        prog="trimlib.py", description="Remove unused imports")
    
    parser.add_argument("-l", '--location', dest='file_location',
                        help="Location of Target file", required= True)
    
    try:
        parser.error = print_error
        args = parser.parse_args()
        if not args.file_location:
            print_error()
        else:
            return args.file_location
    except:
        print("Please provide the file location.")
    