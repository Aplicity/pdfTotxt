import os.path
from pdfminer.pdfparser import  PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed


def pdf2txt(pdf_fileName, output_fileName=None):
    '''
    pdf文档提取文本，并保存到txt文件中。
    pdf_fileName : pdf文件名
    output_fileName: txt文件名，默认为 pdf_fileName 去掉.pdf 换成 .txt
    '''
    if output_fileName is None:
        output_fileName = pdf_fileName.split(".pdf")[0] + '.txt'

    fp = open(pdf_fileName, 'rb')
    # 用文件对象创建一个PDF文档分析器
    parser = PDFParser(fp)

    # 创建一个PDF文档
    doc = PDFDocument()

    # 连接分析器，与文档对象
    parser.set_document(doc)
    doc.set_parser(parser)

    # 提供初始化密码，如果没有密码，就创建一个空的字符串
    doc.initialize()

    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed

    else:
        # 创建PDF，资源管理器，来共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释其对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # 循环遍历列表，每次处理一个page内容
        # doc.get_pages() 获取page列表
        for page in doc.get_pages():
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象
            # 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等
            # 想要获取文本就获得对象的text属性，
            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):
                    with open(output_fileName, 'a') as f:
                        results = x.get_text()
                        f.write(results + "\n")
    # print(results)
    print("file --", pdf_fileName, "Done !")


if __name__ == "__main__":
    pdf_fileName = 'nlp-intro-v1.0.pdf'
    pdf2txt(pdf_fileName)