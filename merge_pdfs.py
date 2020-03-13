import argparse
from PyPDF2 import PdfFileReader, PdfFileWriter
import os
import logging
import sys

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

def merge_pdfs(paths, output):
    """
    Script Kiddie'd from https://realpython.com/pdf-python/#how-to-merge-pdfs
    """
    pdf_writer = PdfFileWriter()

    for path in paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            # Add each page to the writer object
            log.debug(f'Adding page {page} of {path}.')
            pdf_writer.addPage(pdf_reader.getPage(page))

    # Write out the merged PDF
    with open(output, 'wb') as out:
        pdf_writer.write(out)




def get_arg_parser():
    """
    Instantiates the arg parser for this script
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--directory",
        type=str,
        required=False,
        default=".",
        help="The directory to look in for pdfs to merge",
    )
    parser.add_argument("-o", "--output", type=str, required=False, default="out.pdf", help="The name of the output file.")

    return parser

if __name__ == "__main__":
    args = get_arg_parser().parse_args()

    paths = [os.path.join(args.directory, file) for file in os.listdir(args.directory) if '.pdf' in file and file != args.output]
    log.info(f"Paths to merge: {paths}")
    if paths:
        merge_pdfs(paths, output=args.output)
        log.info(f"Finished! Wrote output to: {args.output}")
    else:
        log.warning("No mergable files found!")