#!/usr/bin/python3

import os
from PyPDF2 import PdfMerger

AUDIT_DIR = "audit"

def build_hash(month):
    # Filter for PDFs only
    pdfs = [ file for file in os.listdir(month) if os.path.splitext(file)[1] == '.pdf' ]

    receipts = {}
    coverpages = {}
    workdir = os.getcwd()
    for file in pdfs:
        basefile = os.path.basename(file)
        fullpath = os.path.join( workdir, month, basefile )
        if basefile.split("_")[0] == "cover":
            receipt_name = basefile.split("_")[1]
            coverpages[ receipt_name ]= fullpath        
        else:
            receipts[basefile] = fullpath

    return (receipts, coverpages)

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
            rec, covers = build_hash(month_dir)
            print(rec, covers)
            build_pdf(rec, covers, month_dir)
