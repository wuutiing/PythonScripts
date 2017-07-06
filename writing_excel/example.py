import xlwt
import xlrd
from xlutils.copy import copy
import os

'''
示例演示了如何重写已有的excel文件，需要xlwt，xlrd以及xlutils包支持，
author: wuting
create_time: 2017-07-03
contact: quzhouwuting@163.com
'''



def generate_index_column_style():
    '''
    创建style，加粗及黑色边框'''
    borders = xlwt.Borders() # Create Borders
    borders.left = xlwt.Borders.THIN # May be: NO_LINE, THIN, MEDIUM,DASHED, DOTTED, THICK, DOUBLE, HAIR, MEDIUM_DASHED,THIN_DASH_DOTTED, MEDIUM_DASH_DOTTED, THIN_DASH_DOT_DOTTED,MEDIUM_DASH_DOT_DOTTED, SLANTED_MEDIUM_DASH_DOTTED, or 0x00 through0x0D.
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    borders.bottom = xlwt.Borders.THIN
    borders.left_colour = 0x40
    borders.right_colour = 0x40
    borders.top_colour = 0x40
    borders.bottom_colour = 0x40
    font = xlwt.Font() # Create the Font
    font.bold = True
    style = xlwt.XFStyle() # Create the Style
    style.font = font # Apply the Font to the Style
    style.borders = borders # Add Borders to Style
    # style = xlwt.easyxf('font: color-index red, bold on')
    return style

def create_file(file_path):
    '''
    构建文件，内容99乘法表'''
    index_style = generate_index_column_style()

    workbook = xlwt.Workbook()
    sheet1 = workbook.add_sheet("测试1", cell_overwrite_ok=True)
    sheet2 = workbook.add_sheet("测试2")

    for i in range(100):
        for j in range(100):
            sheet1.write(i, j, i*j)
    for i in range(100):
        sheet1.write(i, 0, i, style=index_style)
    for j in range(100):
        sheet1.write(0, j, j, style=index_style)
    workbook.save(file_path)

def override_file(file_path):
    '''
    在传入文件所路径下新建名后缀_override的xls文件'''
    split_file_path = file_path.split("/")[:-1]
    split_file_path.append(file_path.split("/")[-1].split(".")[0] + "_override.xls")
    new_file_path = "/".join(split_file_path)

    file = xlrd.open_workbook(file_path, formatting_info=True)
    workbook = copy(file)
    sheet1 = workbook.get_sheet(0) # 可以通过sheet的位置顺序获取
    sheet1.write(0, 0, "www")
    sheet1.write(1, 1, "qqq")
    sheet2 = workbook.get_sheet("测试2") # 可以通过sheet的名称获取
    sheet2.write(0, 0, "123")
    workbook.save(new_file_path)



if __name__ == "__main__":
    file_path = os.path.join(os.getcwd(), "test_excel.xls")
    # create_file(file_path)
    override_file(file_path)

