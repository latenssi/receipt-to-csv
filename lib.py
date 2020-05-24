import re
import csv
import PyPDF2

ITEMS_START = 5

item_reg = re.compile(r'^(?P<item>.*)\s+(?P<price>[\d\.]+)\s$', re.I)
spec_reg = re.compile(r'\s{2,}')

def parse_pdf(fileobj):
    pdf_reader = PyPDF2.PdfFileReader(fileobj)
    page_obj = pdf_reader.getPage(0)
    lines = page_obj.extractText().splitlines()

    result = []
    for i in range(ITEMS_START, len(lines)):
        line = lines[i]
        if line.startswith("          "):
            # End of receipt
            break

        if line.startswith(" "):
            # Item count specifier etc.
            result[-1]["specifier"] = spec_reg.sub(', ', line.lstrip())
            continue

        parsed = item_reg.match(line).groupdict()
        parsed['item'] = parsed['item'].rstrip()
        parsed['price'] = float(parsed['price'])

        result.append(parsed)

    return result

def write_csv_buffer(output, data):
    fieldnames = ['item', 'specifier', 'price']
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writerows(data)

def write_csv(filename, data):
    with open(filename, 'w', newline='') as csvfile:
        write_csv_buffer(csvfile, data)
