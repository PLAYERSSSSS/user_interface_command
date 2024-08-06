import decimal

from UIC.module.craft.template import template
from UIC.utils import ANSI


# 如同屎一般的代码
class BarString:
    def __init__(self, array: list[str], color, bg):
        self.text = array
        self.color = ANSI.getRGB_ANSI_String(color)
        self.bg = ANSI.getRGB_ANSI_String_back(bg)
        self.len = f"{array[0]}{array[2]}{array[4]}{array[5]}".__len__()

    def setLen(self, v: int):
        self.len = v

    def getSlice(self, e):
        text = "\033[0m"
        array = [self.text[0], self.text[2], self.text[4], self.text[5]]
        for index, i in enumerate(array):
            if e == 0:
                return text
            if index == 0:
                text += self.color + self.bg
            elif index == 1:
                text += self.text[1] + self.bg
            elif index == 2:
                text += self.text[3] + self.bg
            elif index == 3:
                text += self.color + self.bg
            for k in i:
                if e >= len(k):
                    e -= len(k)
                    text += k[: e]
                else:
                    text += k[: e]
                    return text
        return text

    def __len__(self):
        return self.len

    def __str__(self):
        return self.getSlice(self.len + 1)


class Bar(template):
    def __init__(self, head: str = "", end: str = "", fill="█", size: int = 10):
        self._backColor_ = (0, 0, 0)
        self._color_ = (255, 255, 255)
        self.size = size
        self.head = head
        self.end = end
        self.fill = fill
        self.value = 0
        self.BarColor = (0, 204, 51)
        self.rBarColor = (110, 110, 110)
        self.maintainItsOwnFormat = None
        self._NumericalRangeError_ = ValueError("the value range can only be between 0 and 100.")
        super().__init__(self.getBar().__str__(), color=self._color_, bg=self._backColor_)
        super()._setIsSelected_(False)

    def setBarColor(self, RGB: (int, int, int)):
        self._backColor_ = RGB

    def setrBarColor(self, RGB: (int, int, int)):
        self.rBarColor = RGB

    def setFill(self, fill: str):
        self.fill = fill

    def setSize(self, v: int):
        self.size = v

    def setValue(self, v: int):
        if 0 <= v <= 100:
            self.value = v
        else:
            raise ValueError(self._NumericalRangeError_)

    def addValue(self, v: int):
        if 0 <= (result := v + self.value) <= 100:
            self.value = result
        else:
            raise ValueError(f"{self._NumericalRangeError_} + {str(float(result))}")

    def removeValue(self, v: int):
        if 0 <= (result := self.value - v) <= 100:
            self.value = result
        else:
            raise ValueError(self._NumericalRangeError_)

    def getBar(self):
        pace = int(
            (decimal.Decimal(self.value) / 100) * self.size)
        return BarString([self.head, ANSI.getRGB_ANSI_String(self.BarColor), pace * self.fill,
                          ANSI.getRGB_ANSI_String(self.rBarColor), (self.size - pace) * self.fill, self.end],
                         self.getColor(), self.getBackColor())

    def getText(self):
        return self.getBar()
