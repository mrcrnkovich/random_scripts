#!/usr/bin/python3

import os
import re
from PyPDF2 import PdfMerger
from img2pdf import convert, get_layout_fun, in_to_pt

AUDIT_DIR = "audit"

def build_hash(month):
    # Filter for PDFs only
    pdfs = [ file for file in os.listdir(month) if os.path.splitext(file)[1] == '.pdf']

    receipt_re = re.compile(r'(?P<name>.*)Pink.pdf')

    receipts = {}
    coverpages = {}
    workdir = os.getcwd()
    for file in pdfs:
        basefile = os.path.basename(file)
        fullpath = os.path.join( workdir, month, basefile )

        m = receipt_re.match(basefile)
        if m:
            receipt_name = m.group("name")
            coverpages[ receipt_name + ".pdf" ]= fullpath        
        else:
            receipts[basefile] = fullpath

    return (receipts, coverpages)

def png_to_pdf(month):
    # Filter for PDFs only
    pdfs = [ file for file in os.listdir(month) if os.path.splitext(file)[1] == '.png']

    workdir = os.getcwd()
    for file in pdfs:
        basefile = os.path.splitext(file)[0] # Strip trailing extension .pdf or .png
        fullpath = os.path.join( workdir, month, basefile )

        # specify paper size (A4)
        letter = (in_to_pt(8.5),in_to_pt(11))
        layout_fun = get_layout_fun(letter)
        with open(fullpath + ".pdf", "wb") as pdf:
            pdf.write(convert(fullpath + ".png", layout_fun = layout_fun))

def build_pdf(receipts, coverpages, month_dir):
    merge = PdfMerger()
    output_path = os.path.join( os.getcwd(), AUDIT_DIR, month_dir)

    if not os.path.exists(output_path):
        os.mkdir(output_path)
    for k,v in coverpages.items():
        print( receipts[k], v )
        merge.append( v )
        merge.append( receipts[k] )
        merge.write( os.path.join( output_path, k ))
    merge.close()


if __name__ == '__main__':
    months = [ x for x in os.listdir() if x != AUDIT_DIR ]

    if not os.path.exists(AUDIT_DIR):
        os.mkdir(AUDIT_DIR)
    for month_dir in months:
        if os.path.isdir(month_dir):
            png_to_pdf(month_dir)
            rec, covers = build_hash(month_dir)
            print(rec, covers)
            build_pdf(rec, covers, month_dir)
