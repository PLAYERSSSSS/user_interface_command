class template:
    def __init__(self, text: str, bg=(0, 0, 0), color=(255, 255, 255)):
        self._isSelected_ = True
        self._text_ = text
        self._color_ = color
        self._backColor_ = bg
        self._hoveText_ = text
        self._hoveColor_ = (255, 255, 255)
        self._hoveBackColor_ = (0, 0, 0)

    def getIsSelected(self):
        return self._isSelected_

    def _setIsSelected_(self, v):
        self._isSelected_ = v

    def setColor(self, RGB: (int, int, int)):
        self._color_ = RGB

    def setBackColor(self, RGB: (int, int, int)):
        self._backColor_ = RGB

    def setHoveColor(self, RGB: (int, int, int)):
        self._hoveColor_ = RGB

    def setHoveBackColor(self, RGB: (int, int, int)):
        self._hoveBackColor_ = RGB

    def setText(self, text: str):
        self._text_ = text

    def setHoveText(self, text: str):
        self._hoveText_ = text

    def getText(self):
        return self._text_

    def getHoveText(self):
        return self._hoveText_

    def getColor(self):
        return self._color_

    def getBackColor(self):
        return self._backColor_

    def getHoveColor(self):
        return self._hoveColor_

    def getHoveBackColor(self):
        return self._hoveBackColor_
