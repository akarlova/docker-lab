import csv
import sys

MAX_ROWS = 20


def detect_delimiter(sample):
    try:
        return csv.Sniffer().sniff(sample, delimiters=",;\t").delimiter
    except csv.Error:
        return ","


def describe(delimiter):
    names = {",": "comma (,)", ";": "semicolon (;)", "\t": "tab"}
    return names.get(delimiter, delimiter)


def format_row(values, widths):
    cells = []
    for j, width in enumerate(widths):
        value = values[j] if j < len(values) else ""
        cells.append(value.ljust(width))
    return " | ".join(cells)


def print_table(header, rows):
    shown = rows[:MAX_ROWS]
    widths = [len(name) for name in header]
    for row in shown:
        for j in range(len(header)):
            if j < len(row):
                widths[j] = max(widths[j], len(row[j]))

    print(format_row(header, widths))
    print("-+-".join("-" * w for w in widths))
    for row in shown:
        print(format_row(row, widths))

    if len(rows) > MAX_ROWS:
        print(f"... and {len(rows) - MAX_ROWS} more rows")


def main():
    file_name = sys.argv[1] if len(sys.argv) > 1 else "data.csv"

    try:
        with open(file_name, encoding="utf-8-sig", newline="") as f:
            sample = f.read(4096)  
            f.seek(0)             
            delimiter = detect_delimiter(sample)
            all_rows = [row for row in csv.reader(f, delimiter=delimiter) if row]
    except OSError as e:
        print(f"Error reading file: {e}")
        return

    if not all_rows:
        print("File is empty")
        return

    header = all_rows[0]
    rows = all_rows[1:]

    print(f"File:      {file_name}")
    print(f"Delimiter: {describe(delimiter)}")
    print(f"Columns:   {len(header)}")
    print(f"Rows:      {len(rows)}")
    print()

    print_table(header, rows)


if __name__ == "__main__":
    main()