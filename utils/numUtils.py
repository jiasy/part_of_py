# !/usr/bin/env python3
import math


def getColLineNum(num_):
    '''
        将一个数拆分成 A X B 的形式，长宽比在 3 内的方阵。
            0:0x0,1:1x1,2:2x1,3:3x1,4:2x2,5:5x1,
            6:3x2,7:7x1,8:4x2,9:3x3,10:5x2,
            11:0x0,12:4x3,13:0x0,14:0x0,15:5x3,
            16:4x4,17:0x0,18:6x3,19:0x0,20:5x4,
            21:7x3,22:0x0,23:0x0,24:6x4,25:5x5,
            26:0x0,27:9x3,28:7x4,29:0x0,30:6x5,
            31:0x0,32:8x4,33:0x0,34:0x0,35:7x5,
            36:6x6,37:0x0,38:0x0,39:0x0,40:8x5,
            41:0x0,42:7x6,43:0x0,44:11x4,45:9x5,
            46:0x0,47:0x0,48:8x6,49:7x7,50:10x5
    '''
    if num_ <= 0:
        return 0, 0
    _lineCurrent = math.floor(math.sqrt(num_))
    while True:
        _column = math.floor(num_ / _lineCurrent)
        if _column >= _lineCurrent:
            _lineCountYu = num_ % _lineCurrent
            if _lineCountYu == 0:
                _line = _lineCurrent
                if num_ > 10 and _column / _line > 3:
                    return 0, 0
                return _column, _line
        _lineCurrent -= 1
        if _lineCurrent == 0:
            return 0, 0
