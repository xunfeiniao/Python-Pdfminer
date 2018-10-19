from io import StringIO

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import os
import sys, getopt


# converts pdf, returns its text content as a string
# from https://www.binpress.com/tutorial/manipulating-pdfs-with-python/167
from pdfminer.pdfparser import PDFParser

def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(fname,'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text


# converts all pdfs in directory pdfDir, saves all resulting txt files to txtdir
def convertMultiple(pdfDir, txtDir):
    if os.path.exists(txtDir):
        pass
    else:
        os.makedirs(txtDir)
    if pdfDir == "": pdfDir = os.getcwd() + "\\"  # if no pdfDir passed in
    for pdf in os.listdir(pdfDir):  # iterate through pdfs in pdf directory
        fileExtension = pdf.split(".")[-1]
        if fileExtension == "pdf" or fileExtension == "PDF":
            pdfFilename = pdfDir + pdf
            text = convert(pdfFilename)  # get string of text content of pdf
            textFilename = txtDir + '\\' +pdf[:-4]+ ".txt"
            f = open(textFilename,'a',encoding='utf-8')
            f.write(text)
            f.close()
# i : info
# p : pdfDir
# t = txtDir
def PDFTOTXT(argv):
    try:
        #opts是指拿到argv中必须拿到的参数，args是argv中不需要的参数
        opts, args = getopt.getopt(argv, "ip:t:")
    except getopt.GetoptError:
        print("pdfToT.py -p <pdfdirectory> -t <textdirectory>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-i":
            print("pdfToT.py -p <pdfdirectory> -t <textdirectory>")
            sys.exit()
        elif opt == "-p":
            pdfDir = arg
        elif opt == "-t":
            txtDir = arg
    convertMultiple(pdfDir,txtDir)


if __name__ == "__main__":
    PDFTOTXT(sys.argv[1:])