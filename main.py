import sys
import lib

def main():
    filename = sys.argv[1]
    with open(filename, 'rb') as pdffile:
        result = lib.parse_pdf(pdffile)

    lib.write_csv(filename.replace(".pdf", ".csv"), result)

if __name__ == "__main__":
    main()
