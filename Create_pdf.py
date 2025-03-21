from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def create_pdf():
    # 创建一个 PDF 文件对象
    c = canvas.Canvas("example.pdf", pagesize=letter)

    # 在 PDF 上添加文本
    c.drawString(100, 750, "Hello, this is a simple PDF created with ReportLab.")

    # 保存 PDF 文件
    c.save()


if __name__ == "__main__":
    create_pdf()