import win32print
import win32ui
from PIL import Image, ImageWin

# printer_name是默认打印机的名字
printer_name = win32print.GetDefaultPrinter()
# 调用打印机打印两张图片
for i in range(2):
    hDC = win32ui.CreateDC()
    hDC.CreatePrinterDC(printer_name)

    # 打开图片
    bmp = Image.open("C:\\Users\\DeepForest\\Desktop\\28610063816.pdf")

    scale = 1
    w, h = bmp.size
    hDC.StartDoc("C:\\Users\\DeepForest\\Desktop\\28610063816.pdf")
    hDC.StartPage()

    dib = ImageWin.Dib(bmp)

    # (10,10,1024,768)前面的两个数字是坐标，后面两个数字是打印纸张的大小
    dib.draw(hDC.GetHandleOutput(), (10, 10, 1024*2, 768*2))

    hDC.EndPage()
    hDC.EndDoc()
hDC.DeleteDC()
