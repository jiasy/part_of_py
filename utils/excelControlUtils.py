# !/usr/bin/env python3
import os.path
import xlwings
from xlwings import constants
from utils import fileUtils
from utils import cmdUtils
from utils import printUtils
import sys
import math
from appscript import app
import xlwings as xw
from xlwings.base_classes import Book
from xlwings.constants import ChartType

'''
开启 xlwings 对 Excel 的控制，这里就可以自动居中显示（否则只是选中，不会在Excel界面中摆放到居中位置）。
base : 
    which xlwings - 查看是否安装（有的话，就有路径显示）。
    xlwings addin install - 安装对 Excel 的控制，mac下会有提示，同意即可。
'''
chatTypeList = [
    '3d_area', '3d_area_stacked', '3d_area_stacked_100', '3d_bar_clustered', '3d_bar_stacked', '3d_bar_stacked_100',
    '3d_column', '3d_column_clustered', '3d_column_stacked', '3d_column_stacked_100', '3d_line', '3d_pie',
    '3d_pie_exploded', 'area', 'area_stacked', 'area_stacked_100', 'bar_clustered', 'bar_of_pie', 'bar_stacked',
    'bar_stacked_100', 'bubble', 'bubble_3d_effect', 'column_clustered', 'column_stacked', 'column_stacked_100',
    'cone_bar_clustered', 'cone_bar_stacked', 'cone_bar_stacked_100', 'cone_col', 'cone_col_clustered',
    'cone_col_stacked', 'cone_col_stacked_100', 'cylinder_bar_clustered', 'cylinder_bar_stacked',
    'cylinder_bar_stacked_100', 'cylinder_col', 'cylinder_col_clustered', 'cylinder_col_stacked',
    'cylinder_col_stacked_100', 'doughnut', 'doughnut_exploded', 'line', 'line_markers', 'line_markers_stacked',
    'line_markers_stacked_100', 'line_stacked', 'line_stacked_100', 'pie', 'pie_exploded', 'pie_of_pie',
    'pyramid_bar_clustered', 'pyramid_bar_stacked', 'pyramid_bar_stacked_100', 'pyramid_col', 'pyramid_col_clustered',
    'pyramid_col_stacked', 'pyramid_col_stacked_100', 'radar', 'radar_filled', 'radar_markers',

    # 'stock_hlc'# 'stock_ohlc'# 'stock_vhlc'# 'stock_vohlc'# 'surface'# 'surface_top_view'# 'surface_top_view_wireframe'# 'surface_wireframe',

    'xy_scatter', 'xy_scatter_lines', 'xy_scatter_lines_no_markers', 'xy_scatter_smooth',
    'xy_scatter_smooth_no_markers']

colorNameList = ["rgbAliceBlue", "rgbAntiqueWhite", "rgbAqua", "rgbAquamarine", "rgbAzure", "rgbBeige", "rgbBisque",
                 "rgbBlack", "rgbBlanchedAlmond", "rgbBlue", "rgbBlueViolet", "rgbBrown", "rgbBurlyWood",
                 "rgbCadetBlue",
                 "rgbChartreuse", "rgbCoral", "rgbCornflowerBlue", "rgbCornsilk", "rgbCrimson", "rgbDarkBlue",
                 "rgbDarkCyan", "rgbDarkGoldenrod", "rgbDarkGray", "rgbDarkGreen", "rgbDarkGrey", "rgbDarkKhaki",
                 "rgbDarkMagenta", "rgbDarkOliveGreen", "rgbDarkOrange", "rgbDarkOrchid", "rgbDarkRed", "rgbDarkSalmon",
                 "rgbDarkSeaGreen", "rgbDarkSlateBlue", "rgbDarkSlateGray", "rgbDarkSlateGrey", "rgbDarkTurquoise",
                 "rgbDarkViolet", "rgbDeepPink", "rgbDeepSkyBlue", "rgbDimGray", "rgbDimGrey", "rgbDodgerBlue",
                 "rgbFireBrick", "rgbFloralWhite", "rgbForestGreen", "rgbFuchsia", "rgbGainsboro", "rgbGhostWhite",
                 "rgbGold", "rgbGoldenrod", "rgbGray", "rgbGreen", "rgbGreenYellow", "rgbGrey", "rgbHoneydew",
                 "rgbHotPink",
                 "rgbIndianRed", "rgbIndigo", "rgbIvory", "rgbKhaki", "rgbLavender", "rgbLavenderBlush", "rgbLawnGreen",
                 "rgbLemonChiffon", "rgbLightBlue", "rgbLightCoral", "rgbLightCyan", "rgbLightGoldenrodYellow",
                 "rgbLightGray", "rgbLightGreen", "rgbLightGrey", "rgbLightPink", "rgbLightSalmon", "rgbLightSeaGreen",
                 "rgbLightSkyBlue", "rgbLightSlateGray", "rgbLightSlateGrey", "rgbLightSteelBlue", "rgbLightYellow",
                 "rgbLime", "rgbLimeGreen", "rgbLinen", "rgbMaroon", "rgbMediumAquamarine", "rgbMediumBlue",
                 "rgbMediumOrchid", "rgbMediumPurple", "rgbMediumSeaGreen", "rgbMediumSlateBlue",
                 "rgbMediumSpringGreen",
                 "rgbMediumTurquoise", "rgbMediumVioletRed", "rgbMidnightBlue", "rgbMintCream", "rgbMistyRose",
                 "rgbMoccasin", "rgbNavajoWhite", "rgbNavy", "rgbNavyBlue", "rgbOldLace", "rgbOlive", "rgbOliveDrab",
                 "rgbOrange", "rgbOrangeRed", "rgbOrchid", "rgbPaleGoldenrod", "rgbPaleGreen", "rgbPaleTurquoise",
                 "rgbPaleVioletRed", "rgbPapayaWhip", "rgbPeachPuff", "rgbPeru", "rgbPink", "rgbPlum", "rgbPowderBlue",
                 "rgbPurple", "rgbRed", "rgbRosyBrown", "rgbRoyalBlue", "rgbSalmon", "rgbSandyBrown", "rgbSeaGreen",
                 "rgbSeashell", "rgbSienna", "rgbSilver", "rgbSkyBlue", "rgbSlateBlue", "rgbSlateGray", "rgbSlateGrey",
                 "rgbSnow", "rgbSpringGreen", "rgbSteelBlue", "rgbTan", "rgbTeal", "rgbThistle", "rgbTomato",
                 "rgbTurquoise", "rgbViolet", "rgbWheat", "rgbWhite", "rgbWhiteSmoke", "rgbYellow", "rgbYellowGreen"]
colorList = [constants.RgbColor.rgbAliceBlue, constants.RgbColor.rgbAntiqueWhite, constants.RgbColor.rgbAqua,
             constants.RgbColor.rgbAquamarine, constants.RgbColor.rgbAzure, constants.RgbColor.rgbBeige,
             constants.RgbColor.rgbBisque, constants.RgbColor.rgbBlack, constants.RgbColor.rgbBlanchedAlmond,
             constants.RgbColor.rgbBlue, constants.RgbColor.rgbBlueViolet, constants.RgbColor.rgbBrown,
             constants.RgbColor.rgbBurlyWood, constants.RgbColor.rgbCadetBlue, constants.RgbColor.rgbChartreuse,
             constants.RgbColor.rgbCoral, constants.RgbColor.rgbCornflowerBlue, constants.RgbColor.rgbCornsilk,
             constants.RgbColor.rgbCrimson, constants.RgbColor.rgbDarkBlue, constants.RgbColor.rgbDarkCyan,
             constants.RgbColor.rgbDarkGoldenrod, constants.RgbColor.rgbDarkGray, constants.RgbColor.rgbDarkGreen,
             constants.RgbColor.rgbDarkGrey, constants.RgbColor.rgbDarkKhaki, constants.RgbColor.rgbDarkMagenta,
             constants.RgbColor.rgbDarkOliveGreen, constants.RgbColor.rgbDarkOrange, constants.RgbColor.rgbDarkOrchid,
             constants.RgbColor.rgbDarkRed, constants.RgbColor.rgbDarkSalmon, constants.RgbColor.rgbDarkSeaGreen,
             constants.RgbColor.rgbDarkSlateBlue, constants.RgbColor.rgbDarkSlateGray,
             constants.RgbColor.rgbDarkSlateGrey, constants.RgbColor.rgbDarkTurquoise, constants.RgbColor.rgbDarkViolet,
             constants.RgbColor.rgbDeepPink, constants.RgbColor.rgbDeepSkyBlue, constants.RgbColor.rgbDimGray,
             constants.RgbColor.rgbDimGrey, constants.RgbColor.rgbDodgerBlue, constants.RgbColor.rgbFireBrick,
             constants.RgbColor.rgbFloralWhite, constants.RgbColor.rgbForestGreen, constants.RgbColor.rgbFuchsia,
             constants.RgbColor.rgbGainsboro, constants.RgbColor.rgbGhostWhite, constants.RgbColor.rgbGold,
             constants.RgbColor.rgbGoldenrod, constants.RgbColor.rgbGray, constants.RgbColor.rgbGreen,
             constants.RgbColor.rgbGreenYellow, constants.RgbColor.rgbGrey, constants.RgbColor.rgbHoneydew,
             constants.RgbColor.rgbHotPink, constants.RgbColor.rgbIndianRed, constants.RgbColor.rgbIndigo,
             constants.RgbColor.rgbIvory, constants.RgbColor.rgbKhaki, constants.RgbColor.rgbLavender,
             constants.RgbColor.rgbLavenderBlush, constants.RgbColor.rgbLawnGreen, constants.RgbColor.rgbLemonChiffon,
             constants.RgbColor.rgbLightBlue, constants.RgbColor.rgbLightCoral, constants.RgbColor.rgbLightCyan,
             constants.RgbColor.rgbLightGoldenrodYellow, constants.RgbColor.rgbLightGray,
             constants.RgbColor.rgbLightGreen, constants.RgbColor.rgbLightGrey, constants.RgbColor.rgbLightPink,
             constants.RgbColor.rgbLightSalmon, constants.RgbColor.rgbLightSeaGreen, constants.RgbColor.rgbLightSkyBlue,
             constants.RgbColor.rgbLightSlateGray, constants.RgbColor.rgbLightSlateGrey,
             constants.RgbColor.rgbLightSteelBlue, constants.RgbColor.rgbLightYellow, constants.RgbColor.rgbLime,
             constants.RgbColor.rgbLimeGreen, constants.RgbColor.rgbLinen, constants.RgbColor.rgbMaroon,
             constants.RgbColor.rgbMediumAquamarine, constants.RgbColor.rgbMediumBlue,
             constants.RgbColor.rgbMediumOrchid, constants.RgbColor.rgbMediumPurple,
             constants.RgbColor.rgbMediumSeaGreen, constants.RgbColor.rgbMediumSlateBlue,
             constants.RgbColor.rgbMediumSpringGreen, constants.RgbColor.rgbMediumTurquoise,
             constants.RgbColor.rgbMediumVioletRed, constants.RgbColor.rgbMidnightBlue, constants.RgbColor.rgbMintCream,
             constants.RgbColor.rgbMistyRose, constants.RgbColor.rgbMoccasin, constants.RgbColor.rgbNavajoWhite,
             constants.RgbColor.rgbNavy, constants.RgbColor.rgbNavyBlue, constants.RgbColor.rgbOldLace,
             constants.RgbColor.rgbOlive, constants.RgbColor.rgbOliveDrab, constants.RgbColor.rgbOrange,
             constants.RgbColor.rgbOrangeRed, constants.RgbColor.rgbOrchid, constants.RgbColor.rgbPaleGoldenrod,
             constants.RgbColor.rgbPaleGreen, constants.RgbColor.rgbPaleTurquoise, constants.RgbColor.rgbPaleVioletRed,
             constants.RgbColor.rgbPapayaWhip, constants.RgbColor.rgbPeachPuff, constants.RgbColor.rgbPeru,
             constants.RgbColor.rgbPink, constants.RgbColor.rgbPlum, constants.RgbColor.rgbPowderBlue,
             constants.RgbColor.rgbPurple, constants.RgbColor.rgbRed, constants.RgbColor.rgbRosyBrown,
             constants.RgbColor.rgbRoyalBlue, constants.RgbColor.rgbSalmon, constants.RgbColor.rgbSandyBrown,
             constants.RgbColor.rgbSeaGreen, constants.RgbColor.rgbSeashell, constants.RgbColor.rgbSienna,
             constants.RgbColor.rgbSilver, constants.RgbColor.rgbSkyBlue, constants.RgbColor.rgbSlateBlue,
             constants.RgbColor.rgbSlateGray, constants.RgbColor.rgbSlateGrey, constants.RgbColor.rgbSnow,
             constants.RgbColor.rgbSpringGreen, constants.RgbColor.rgbSteelBlue, constants.RgbColor.rgbTan,
             constants.RgbColor.rgbTeal, constants.RgbColor.rgbThistle, constants.RgbColor.rgbTomato,
             constants.RgbColor.rgbTurquoise, constants.RgbColor.rgbViolet, constants.RgbColor.rgbWheat,
             constants.RgbColor.rgbWhite, constants.RgbColor.rgbWhiteSmoke, constants.RgbColor.rgbYellow,
             constants.RgbColor.rgbYellowGreen]
useColorList = [constants.RgbColor.rgbYellowGreen, constants.RgbColor.rgbYellow, constants.RgbColor.rgbViolet,
                constants.RgbColor.rgbTomato, constants.RgbColor.rgbThistle, constants.RgbColor.rgbTurquoise,
                constants.RgbColor.rgbSkyBlue, constants.RgbColor.rgbSandyBrown, constants.RgbColor.rgbPowderBlue,
                constants.RgbColor.rgbChartreuse, constants.RgbColor.rgbCornflowerBlue, constants.RgbColor.rgbBurlyWood,
                constants.RgbColor.rgbDarkGrey, constants.RgbColor.rgbBrown, constants.RgbColor.rgbMediumOrchid,
                constants.RgbColor.rgbNavajoWhite, constants.RgbColor.rgbGreenYellow]
# Excel 中默认的宽高
_defaultCellWidth = 65
_defaultCellHeight = 16


def numberToColumn(number_):
    if number_ == 0:
        printUtils.pError("ERROR : n 不能是 0")
        sys.exit(1)
    _result = ""
    while number_ > 0:
        number_, remainder = divmod(number_ - 1, 26)
        _result = chr(65 + remainder) + _result
    return _result


def columnToNumber(column: str) -> int:
    result = 0
    for char in column:
        result = result * 26 + (ord(char) - ord('A') + 1)
    return result


# 通过 idx 获得 列的字符
def getCharByIdx(idx_: int):
    return numberToColumn(idx_ + 1)


# 是否已经开了一个Excel
def checkExcelAppIsOpen():
    # 删


# 检测当前是否有多个Excel运行
def checkMultiExcelApp():
    _backStr = cmdUtils.doCmdAndGetPiplineList("lsappinfo", "visibleprocesslist", "-includehidden")
    if isinstance(_backStr, str):
        _appInfoList = _backStr.split(" ")
    else:
        _appInfoList = _backStr[0].split(" ")
    _excelAppName = "Microsoft_Excel"
    _excelAlreadyExit = False
    for _i in range(len(_appInfoList)):
        _appName = _appInfoList[_i].split('"')[1]
        if _excelAppName == _appName:
            if _excelAlreadyExit == True:
                printUtils.pError("ERROR - 多个Excel 开启，执行宏之前，请确保只有一个 Excel 在运行")
                sys.exit(1)
            _excelAlreadyExit = True


def newExcelWorkBook(filePath_: str, defaultSheetName_: str = "sheet_default", front_: bool = True):
    # 删


# 打开指定 Excel 文件，获取其 workBook
def openExcelWorkBook(filePath_: str, front_: bool = True):
    _app = get_active_app()
    if _app is None:
        _app = xlwings.App(visible=front_, add_book=False)  # visible是否可见。False表示后台运行。 add_book 是否新建一个工作簿
    _app.screen_updating = True  # 对Excel操作时，屏幕刷新
    _app.activate(True)  # 激活当前 _app（因为可以同时启动多个app）
    # 通过 Excel App 打开 Excel 文件，返回workBook
    return _app.books.open(filePath_)


def openSheet(filePath_: str, shtName_: str, front_: bool = True):
    _workBook = openExcelWorkBook(filePath_, front_)
    _sheet = _workBook.sheets[shtName_]
    _sheet.activate()
    return _sheet


# 定位到指定的cell
def openCell(filePath_: str, shtName_: str, cell_: str, front_: bool = True):
    _sheet = openSheet(filePath_, shtName_, front_)
    _cell = _sheet[cell_]
    _cell.select()
    return _cell


# 在打开的 WorkBook 中，定位到 sheetName_ 指定的 sheet，选中给定 cell 。
def selectCell(filePath_: str, sheetName_: str, cell_: str, front_: bool = True):
    openCell(filePath_, sheetName_, cell_, front_)


# 在打开的 WorkBook 中，定位到 sheetName_ 指定的 sheet，选中给定行
def selectRow(filePath_: str, sheetName_: str, rowId_: int, front_: bool = True):
    _sheet = openSheet(filePath_, sheetName_, front_)
    row_range = _sheet.range((rowId_, 1), (rowId_, 999))
    row_range.select()
    return row_range


# 起点位置和数列个数
def setRangeColorH(
        xId_: int, yId_: int, count_: int = 1, isUp_: bool = True,
        color_: constants.RgbColor = constants.RgbColor.rgbMediumSeaGreen
):
    if count_ == 0:
        return
    if isUp_:
        xlwings.Range((yId_, xId_), (yId_, xId_ + (count_ - 1))).color = color_
    else:
        xlwings.Range((yId_, xId_ - (count_ - 1)), (yId_, xId_)).color = color_


# 起点位置和数列个数
def setRangeColorV(
        xId_: int, yId_: int, count_: int = 1, isUp_: bool = True,
        color_: constants.RgbColor = constants.RgbColor.rgbMediumSeaGreen
):
    if count_ == 0:
        return

    if isUp_:
        xlwings.Range((yId_ - (count_ - 1), xId_), (yId_, xId_)).color = color_
    else:
        xlwings.Range((yId_, xId_), (yId_ + (count_ - 1), xId_)).color = color_


# 设置一个格子的颜色
def setCellColor(
        xId_: int, yId_: int, color_: constants.RgbColor = constants.RgbColor.rgbMediumSeaGreen
):
    xlwings.Range((xId_, yId_)).color = color_


# cell作为标题
def cellAsTitle(cell_, titleStr_: str, cellColor_=None):
    cell_.value = titleStr_
    cell_.font.bold = True
    cell_.font.color = constants.RgbColor.rgbBlack
    # cell_.font.size
    if cellColor_ != None:
        cell_.color = constants.RgbColor.rgbMediumSeaGreen


def get_active_app():
    try:
        app = xlwings.apps.active
        return app
    except:
        return None


# data_ 为 sht 中的区域 data_
#   列 :（ sht_.range("A1:A100") ）
#   行  （ sht_.range("A1") ）从头到尾
#   行  （ sht_.range("A1").expend() ）从头到尾，从上到下
# idx_ 和 colNum_ 共同决定表格的摆放位置
def drawDefaultChart(chartSht_, data_, idx_: int, title_: str, colNum_: int = 1,
                     chartWidthCellNum_: int = 14, chartHeightCellNum_: int = 16,
                     frameBuffer: int = 4, chartType_: str = 'line'
                     ):
    chartSht_.activate()
    # 竖向一列的摆放
    if colNum_ == 1:
        drawDefaultChartV(chartSht_, data_, idx_, title_, chartWidthCellNum_, chartHeightCellNum_, chartType_)
        return
    # 每一列做一个表
    _chartWidth = _defaultCellWidth * chartWidthCellNum_  # (14 个 Cell 宽)
    _chartHeight = _defaultCellHeight * chartHeightCellNum_  # (25 个 Cell 高）
    _colID = math.floor(idx_ % colNum_ + 1)  # 所在列
    _rowID = math.floor(idx_ / colNum_ + 1)  # 所在行
    _realColID = chartWidthCellNum_ * (_colID - 1) + 1
    _realRowID = (_rowID - 1) * (chartHeightCellNum_ + 1) + 1
    _charStr = getCharByIdx(_realColID - 1)  # 所在列 字符
    # 标题-------------------
    _titleCell = "{}{}".format(_charStr, _realRowID)
    # _chartSheet.range((1, _realColID), (1, _realColID + chartWidthCellNum_)).api.merge()
    cellAsTitle(chartSht_[_titleCell], title_, None)

    chartSht_.range(
        (_realRowID, _realColID),
        (_realRowID + chartHeightCellNum_, _realColID + chartWidthCellNum_ - 1)
    ).color = useColorList[idx_ % len(useColorList)]

    # 画图-------------------
    _chart = chartSht_.charts.add(  # 摆放图位置
        (_colID - 1) * _chartWidth + frameBuffer,
        (_rowID - 1) * _chartHeight + _rowID * chartHeightCellNum_ + frameBuffer
    )
    # SAMPLE - Excel 比较 使用 行做数据源，调用 expand 方法进行 行之间的比较。
    _chart.set_source_data(data_)
    _chart.chart_type = chartType_  # 指定类型
    _chart.width = _chartWidth - 2 * frameBuffer  # 表格大小
    _chart.height = _chartHeight - 2 * frameBuffer


# 纵向一列
#  data_ 为 sht_.range('A3:A12') ,3 - 12 一共 10 个
def drawDefaultChartV(chartSht_, data_, idx_: int, title_: str, chartWidthCellNum_: int, chartHeightCellNum_: int, chartType_: str = 'line'):
    # 每一列做一个表
    _chartWidth = _defaultCellWidth * chartWidthCellNum_
    _chartHeight = _defaultCellHeight * chartHeightCellNum_
    # 画图-------------------
    _colID = chartWidthCellNum_  # 摆放图位置
    _rowID = chartHeightCellNum_ * idx_ + 1
    _charStr = getCharByIdx(_colID)  # 所在列 字符`
    _titleCell = "{}{}".format(_charStr, _rowID)
    cellAsTitle(chartSht_[_titleCell], title_, constants.RgbColor.rgbMediumSeaGreen)
    # 正序排列，1个Cell高度为表格x坐标。新创建的表正好可以挡住x轴文字，进行无缝比较
    _chart = chartSht_.charts.add(0, idx_ * _chartHeight)
    _chart.set_source_data(data_)  # sht_.range('A3:A12') 这样取到的
    _chart.chart_type = chartType_  # 指定类型
    _chart.width = _chartWidth  # 表格大小
    _chart.height = _chartHeight


def drawArrowLine(currentSht_):
    currentSht_.activate()  # 切到指定sheet
    checkMultiExcelApp()  # 执行宏之前，确保只有一个Excel
    app('Microsoft Excel').run_VB_macro('PERSONAL.XLSB!NormalLine')  # 创建箭头
    return currentSht_.shapes[-1]


def drawShape(currentSht_):
    currentSht_.activate()  # 切到指定sheet
    checkMultiExcelApp()  # 执行宏之前，确保只有一个Excel
    app('Microsoft Excel').run_VB_macro('PERSONAL.XLSB!TipFrame')  # 创建Shape
    return currentSht_.shapes[-1]


def createTextRectTangle(excelPath_: str, currentSht_, paramStr_: str):
    _currentHeight = callExcelFunc(excelPath_, 'PERSONAL.XLSB!CreateShapeWithText', currentSht_, paramStr_)
    return int(_currentHeight)


def writeAndMergeCell(excelPath_: str, currentSht_, paramStr_: str):
    callExcelFunc(excelPath_, 'PERSONAL.XLSB!MergeCellsToFitText', currentSht_, paramStr_)


def callExcelFunc(excelPath_: str, excelFunc_: str, targetSheet_, paramStr_: str):
    toExcel(excelPath_, paramStr_)
    targetSheet_.activate()  # 切到指定sheet
    checkMultiExcelApp()  # 执行宏之前，确保只有一个Excel
    app('Microsoft Excel').run_VB_macro(excelFunc_)
    return fromExcel(excelPath_)


# 导出 Personal 的 VBA 模块
def exportPersonalVBAProjectModule(excelPath_: str):
    if not os.path.exists(excelPath_):  # 创建新的 Excel 工作簿，只是为了走现有逻辑用
        _workBook: Book = newExcelWorkBook(excelPath_)
    else:  # 使用现有
        _workBook: Book = openExcelWorkBook(excelPath_)
    app('Microsoft Excel').run_VB_macro('PERSONAL.XLSB!exportPersonalVBAProjectModule')  # 导出 VBA 为 .bas 文件


# 导出 Personal 的 VBA 模块
def importPersonVBAModule(excelPath_: str):
    if not os.path.exists(excelPath_):  # 创建新的 Excel 工作簿，只是为了走现有逻辑用
        _workBook: Book = newExcelWorkBook(excelPath_)
    else:  # 使用现有
        _workBook: Book = openExcelWorkBook(excelPath_)
    app('Microsoft Excel').run_VB_macro('PERSONAL.XLSB!importPersonVBAModule')  # 导入 .bas 为模块


# 导出指定 xlsm 的库
def exportVBAProjectModule(VBAExcelPath_: str, workspaceExcelPath_: str, moduleNameList_: list):
    # 删


# 打开 Excel workbook
def openExclWorkBook(targetExcelPath_: str):
    if targetExcelPath_ is None:
        print(f"ERROR : 请填写Excel路径")
        sys.exit(1)
    if not os.path.exists(targetExcelPath_):  # 创建新的 Excel 工作簿
        _workBook: Book = newExcelWorkBook(targetExcelPath_)
    else:  # 使用现有
        _workBook: Book = openExcelWorkBook(targetExcelPath_)
    return _workBook


# Excel 和 Python 通过文件进行交互
def toExcel(excelPath_, dataStr_: str):
    _folderPath = os.path.split(excelPath_)[0]
    # 移除字符串尾部的空白行（如果存在）
    dataStr_ = dataStr_.rstrip("\n")
    with open(os.path.join(_folderPath, "PythonToExcel.txt"), "w", encoding="gb2312") as file:
        file.write(dataStr_)


def fromExcel(excelPath_):
    _folderPath = os.path.split(excelPath_)[0]
    return fileUtils.readFromFile(os.path.join(_folderPath, "ExcelToPython.txt"))


def clearRuntimeData(excelPath_: str):
    _folderPath = os.path.split(excelPath_)[0]
    fileUtils.writeFileWithStr(os.path.join(_folderPath, "ExcelToPython.txt"), "")
    fileUtils.writeFileWithStr(os.path.join(_folderPath, "PythonToExcel.txt"), "")


# 修改 Sheet 大小
def setAllCellToDefaul(sheet_):
    sheet_.cells.column_width = 1.83
    sheet_.cells.row_height = 16
    sheet_.cells.color = (38, 38, 38)  # 遍历所有单元格并将颜色重置为指定颜色


# 添加一个默认的 Sheet
def addDefaultSheet(workBook_):
    _sheet = workBook_.sheets.add()
    setAllCellToDefaul(_sheet)
    return _sheet


if __name__ == "__main__":
    # CUR_DIR = os.path.abspath('.')
    # 赋值上面的功能名，到这里执行，就可以打开 Excel 并跳转到相应位置。
    # openSheet("bbPJ", "Data数据绑定")

    _letter = numberToColumn(27)
    print('_letter = ' + str(_letter))
    sys.exit(1)

'''
# 图标类型
hart_types_k2s = {
    kw.ThreeD_area: "3d_area",
    kw.ThreeD_area_stacked: "3d_area_stacked",
    kw.ThreeD_area_stacked_100: "3d_area_stacked_100",
    kw.ThreeD_bar_clustered: "3d_bar_clustered",
    kw.ThreeD_bar_stacked: "3d_bar_stacked",
    kw.ThreeD_bar_stacked_100: "3d_bar_stacked_100",
    kw.ThreeD_column: "3d_column",
    kw.ThreeD_column_clustered: "3d_column_clustered",
    kw.ThreeD_column_stacked: "3d_column_stacked",
    kw.ThreeD_column_stacked_100: "3d_column_stacked_100",
    kw.ThreeD_line: "3d_line",
    kw.ThreeD_pie: "3d_pie",
    kw.ThreeD_pie_exploded: "3d_pie_exploded",
    kw.area_chart: "area",
    kw.area_stacked: "area_stacked",
    kw.area_stacked_100: "area_stacked_100",
    kw.bar_clustered: "bar_clustered",
    kw.bar_of_pie: "bar_of_pie",
    kw.bar_stacked: "bar_stacked",
    kw.bar_stacked_100: "bar_stacked_100",
    kw.bubble: "bubble",
    kw.bubble_ThreeD_effect: "bubble_3d_effect",
    kw.column_clustered: "column_clustered",
    kw.column_stacked: "column_stacked",
    kw.column_stacked_100: "column_stacked_100",
    kw.combination_chart: "combination",
    kw.cone_bar_clustered: "cone_bar_clustered",
    kw.cone_bar_stacked: "cone_bar_stacked",
    kw.cone_bar_stacked_100: "cone_bar_stacked_100",
    kw.cone_col: "cone_col",
    kw.cone_column_clustered: "cone_col_clustered",
    kw.cone_column_stacked: "cone_col_stacked",
    kw.cone_column_stacked_100: "cone_col_stacked_100",
    kw.cylinder_bar_clustered: "cylinder_bar_clustered",
    kw.cylinder_bar_stacked: "cylinder_bar_stacked",
    kw.cylinder_bar_stacked_100: "cylinder_bar_stacked_100",
    kw.cylinder_column: "cylinder_col",
    kw.cylinder_column_clustered: "cylinder_col_clustered",
    kw.cylinder_column_stacked: "cylinder_col_stacked",
    kw.cylinder_column_stacked_100: "cylinder_col_stacked_100",
    kw.doughnut: "doughnut",
    kw.doughnut_exploded: "doughnut_exploded",
    kw.line_chart: "line",
    kw.line_markers: "line_markers",
    kw.line_markers_stacked: "line_markers_stacked",
    kw.line_markers_stacked_100: "line_markers_stacked_100",
    kw.line_stacked: "line_stacked",
    kw.line_stacked_100: "line_stacked_100",
    kw.pie_chart: "pie",
    kw.pie_exploded: "pie_exploded",
    kw.pie_of_pie: "pie_of_pie",
    kw.pyramid_bar_clustered: "pyramid_bar_clustered",
    kw.pyramid_bar_stacked: "pyramid_bar_stacked",
    kw.pyramid_bar_stacked_100: "pyramid_bar_stacked_100",
    kw.pyramid_column: "pyramid_col",
    kw.pyramid_column_clustered: "pyramid_col_clustered",
    kw.pyramid_column_stacked: "pyramid_col_stacked",
    kw.pyramid_column_stacked_100: "pyramid_col_stacked_100",
    kw.radar: "radar",
    kw.radar_filled: "radar_filled",
    kw.radar_markers: "radar_markers",
    kw.stock_HLC: "stock_hlc",
    kw.stock_OHLC: "stock_ohlc",
    kw.stock_VHLC: "stock_vhlc",
    kw.stock_VOHLC: "stock_vohlc",
    kw.surface: "surface",
    kw.surface_top_view: "surface_top_view",
    kw.surface_top_view_wireframe: "surface_top_view_wireframe",
    kw.surface_wireframe: "surface_wireframe",
    kw.xy_scatter_lines: "xy_scatter_lines",
    kw.xy_scatter_lines_no_markers: "xy_scatter_lines_no_markers",
    kw.xy_scatter_smooth: "xy_scatter_smooth",
    kw.xy_scatter_smooth_no_markers: "xy_scatter_smooth_no_markers",
    kw.xyscatter: "xy_scatter",
}
'''
