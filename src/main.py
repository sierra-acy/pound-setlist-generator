import argparse
from main_pound import main_pound
from main_pom import main_pom

def main():
    """ main runner """
    
    args = get_args()
    if(args['format'] == 'pound'):
        main_pound()
    else:
        main_pom()

def get_args():
    """ Setup argument parser """
    parser = argparse.ArgumentParser()
    parser.add_argument('-format', required=True, help='class format', choices=['pound', 'pom'])
    return vars(parser.parse_args())

if __name__ == "__main__":
    main()