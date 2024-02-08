import argparse
from model import Company, export_to_csv, import_from_csv

def main():
    parser = argparse.ArgumentParser(description='Export and import data to/from a CSV file.')
    parser.add_argument('command', choices=['export', 'import'], help='The command to execute.')
    parser.add_argument('filename', help='The name of the CSV file to export to or import from.')

    args = parser.parse_args()

    if args.command == 'export':
        export_to_csv(Company, args.filename)
    elif args.command == 'import':
        import_from_csv(Company, args.filename)

if __name__ == '__main__':
    main()