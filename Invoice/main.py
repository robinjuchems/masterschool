import os

def list_files(dir):
    return os.listdir(dir)


def extract_month(filename):
    parts = filename.split('_')
    if len(parts) < 3:
        print(f"Invalid filename: {filename}")
        return None
    month_plus_extension = parts[2]
    if '.' not in month_plus_extension:
        print(f"Invalid filename: {filename}")
        return None
    month = month_plus_extension.split('.')[0]
    return month


def make_folder(month):
    if not os.path.exists(month):
        os.mkdir(month)


def move_file(file, month):
    newpath = os.path.join(month, file)
    os.rename(file, newpath)


def main():
    invoices = list_files('.')

    for invoice in invoices:
        month = extract_month(invoice)
        if month is None:
            continue
        make_folder(month)
        move_file(invoice, month)


if __name__ == '__main__':
    main()