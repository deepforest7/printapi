import win32print
import win32api
fn = 'C:\\Users\\DeepForest\\Desktop\\28610063816.pdf'
win32api.ShellExecute(0,\
                      'print',\
                      fn,\
                      win32print.GetDefaultPrinterW(),\
                      ".",
                      0)
