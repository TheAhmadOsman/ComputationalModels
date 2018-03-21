###########################################
#   Author: Ahmad M. Osman
#   Date: 11/10/2017
#
#   Class: CS 260
#   Instructor: Dr. Kent Lee
#
#   File name: calculator.py
#   Purpose: Calculator Program
###########################################


import calcscanner
import calcparser
import sys
import io


def main():

    # unless testing, it should be sys.stdin
    #strm = io.StringIO("457+321")

    print("Enter expressions with +,-,*,/,S (for store), and R (for recall) and terminated by a semicolon (i.e. ;).")

    strm = sys.stdin
    theScanner = calcscanner.calcScanner(strm)

    '''
    while True:
        tokenId, lex = theScanner.getToken()
        print(tokenId, lex)
        if tokenId == 10:
            return
	'''

    theParser = calcparser.calcParser()

    ast = theParser.parse(theScanner)

    # The calculator output example on the website did not show
    # program termination as a requirement for this program
    # nor did the input requesting output

if __name__ == "__main__":
    main()
