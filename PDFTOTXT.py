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
    # 创建一个PDF资源管理器对象来存储共赏资源
    manager = PDFResourceManager()
    # 创建一个PDF设备对象
    converter = TextConverter(manager, output, laparams=LAParams())
    # 创建一个PDF解释器对象
    interpreter = PDFPageInterpreter(manager, converter)
    
    #打开源pdf文件
    infile = open(fname,'rb')
    
    #对pdf每一页进行分析
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    
    #得到每一页的txt文档
    text = output.getvalue()
    output.close
    return text


# converts all pdfs in directory pdfDir, saves all resulting txt files to txtdir
def convertMultiple(pdfDir, txtDir):
    #判断是否有储存的文件夹，如果有则pass，没有则创建
    if os.path.exists(txtDir):
        pass
    else:
        os.makedirs(txtDir)
    #判断读取pdf是否需要密码
    if pdfDir == "": pdfDir = os.getcwd() + "\\"  # if no pdfDir passed in
        
    #遍历文件夹下每一个pdf文件
    for pdf in os.listdir(pdfDir):  # iterate through pdfs in pdf directory
        fileExtension = pdf.split(".")[-1]
        #判断是否该文件夹下的文件是否是pdf文件
        if fileExtension == "pdf" or fileExtension == "PDF":
            #构建pdf的完全路径
            pdfFilename = pdfDir + pdf
            text = convert(pdfFilename)  # get string of text content of pdf
            #构建存储文件的目标路径
            textFilename = txtDir + '\\' +pdf[:-4]+ ".txt"
            #将解析得到的pdf文件写入对应的txt文件
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
        #解析每一个参数，得到源文件路径和目标文件路径
        if opt == "-i":
            print("pdfToT.py -p <pdfdirectory> -t <textdirectory>")
            sys.exit()
        elif opt == "-p":
            pdfDir = arg
        elif opt == "-t":
            txtDir = arg
    #调用pdf解析文件
    convertMultiple(pdfDir,txtDir)


if __name__ == "__main__":
    PDFTOTXT(sys.argv[1:])
