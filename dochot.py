#!/usr/bin/env python

import os
import argparse
import subprocess
import pyparsing as pp
import pdftotext
import re
from collections import namedtuple
from ofxtools.models import *
from ofxtools.utils import UTC
from decimal import Decimal
from datetime import datetime
import csv
from datetime import datetime

REGEX_STMT = {
    'SC': r'\ (\d{2}\/\d{2})\s+(\d{2}\/\d{2})\s+(\S+)\s+￥(\d+\.\d{2})',
    'HSBC': r'\ (\d{2}\/\d{2})\s+(\d{2}\/\d{2})\s+(\S+)\s+￥(\d+\.\d{2})' 
}

BANK_NAME = {
    '0021': 'SC',
    '0001': 'HSBC'
}


def read_pdf(fname : str):
    """ Read bank statement (PDF) file
    """
    with open(fname, 'rb') as f:
        if not args.passwd:
            pdf = pdftotext.PDF(f)
        else:
            pdf = pdftotext.PDF(f, args.passwd)
    return ''.join(pdf).splitlines()

def extract_transaction(statement : str, bank : str):
    """extraction transactions from PDF file
    """
    trx = namedtuple('trx', ['date', 'payee', 'amount'])
    trx_list = []
    for l in statement:
        transaction = re.match(REGEX_STMT[bank], l)
        if transaction:
            trx_list.append(
                trx(date=transaction.group(1),
                    payee=transaction.group(3),
                    amount=transaction.group(4)
                ))
    return trx_list
        

if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(description="Bank Statement Parser")
    args_parser.add_argument('filename', type=str,
                             help="the statement file")
    args_parser.add_argument('-p', '--passwd', 
                             help="simply just password", type=str)
    # todo(qzhou): verbosity in the programs
    args_parser.add_argument('-v', '--verbosity', action='count', default=0,
                             help="verbosity for troubleshooting")
    args_parser.add_argument('-b', '--bank', help="name of the bank")
    args_parser.add_argument('-t', '--type', help="file type: pdf, html, etc")
    args_parser.add_argument('-o', '--out', help='specify the name of output file',
                             default=None)
    args = args_parser.parse_args()
    stmt = read_pdf(args.filename)
    #todo(qzhou): programmtic bank name determination
    bank_id = os.path.basename(args.filename).split('-')[0]
    bank_name = BANK_NAME[bank_id]
    transactions = extract_transaction(stmt, bank_name)
    out=args.out
    if out == None:
        now = str(datetime.now().strftime('%Y%M%d_%H%M%S'))
        out = os.path.basename(args.filename).split('.')[1] + now + str('.csv')

    with open(out,'w') as f:
        writer = csv.writer(f)
        writer.writerow(['date','payee','amount'])
        for transaction in transactions:
            writer.writerow(transaction)
        


        

    


