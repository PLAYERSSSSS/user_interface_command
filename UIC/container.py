import os
import sys
from concurrent.futures.thread import ThreadPoolExecutor

import keyboard


class Frame:
    def __init__(self, lineNumber: int, columnsNumber: int, threadingPool=ThreadPoolExecutor(max_workers=1),
                 vacancyReplacement: str = None):
        self.isLinux = sys.platform.startswith('linux')
        self.pool = threadingPool
        self.point = [0, 0]
        self.lineNumber = lineNumber
        self.columnsNumber = columnsNumber
        self._structure_ = []
        self._newStructure_(lineNumber, columnsNumber)
        self.text = ""
        self.bg = (0, 0, 0)
        if vacancyReplacement is None:
            self.vacancyReplacement = " " * 8
        else:
            self.vacancyReplacement = vacancyReplacement
        if not self.isLinux:
            os.system("")

        sys.stdout = open(sys.stdout.fileno(), mode='w', buffering=1024 * 10)
        sys.stdout.write("\033c\033[?25l")
        sys.stdout.flush()

    def _newStructure_(self, lineNumber: int, columnsNumber: int):
        self._structure_ = [[None] * columnsNumber for _ in range(lineNumber)]

    def _keyEvent_(self):
        def callback(e: keyboard.KeyboardEvent):
            el = self.getWidget(*self.point)
            isTransmit = True
            if el is not None and hasattr(el, "keyEvent"):
                isTransmit = el.keyEvent(e, self)

            if e.event_type == 'down' and isTransmit:
                i = self.point
                while True:
                    if e.name == "down":
                        if self.point[0] < self.lineNumber - 1:
                            self.point[0] += 1
                        else:
                            self.point = i
                            break
                    elif e.name == "up":
                        if self.point[0] > 0:
                            self.point[0] -= 1
                        else:
                            self.point = i
                            break
                    elif e.name == "right":
                        if self.point[1] < self.columnsNumber - 1:
                            self.point[1] += 1
                        else:
                            self.point = i
                            break
                    elif e.name == "left":
                        if self.point[1] > 0:
                            self.point[1] -= 1
                        else:
                            self.point = i
                            break

                    el = self.getWidget(*self.point)
                    if el is None or el.getIsSelected() == False:
                        continue
                    else:
                        break

                element = self.getWidget(*self.point)
                if element is None or not element.getIsSelected():
                    self.point = i
                    self._rollbackAnOperation_(e)

                if e.name == "enter":
                    if hasattr(element, "press"):
                        element.press()

                self.reset()

        keyboard.on_press(callback)
        keyboard.wait()

    def setBackColor(self, RGB: (int, int, int)):
        self.bg = RGB

    def setStructure(self, structure: list[list]):
        self._structure_ = structure

    def getStructure(self):
        return self._structure_

    def _rollbackAnOperation_(self, e):
        i = self.point
        while True:
            try:
                if e.name == "down":
                    self.point[0] -= 1
                    if self.getWidget(*self.point) is not None and self.getWidget(*self.point).getIsSelected():
                        break
                elif e.name == "up":
                    self.point[0] += 1
                    if self.getWidget(*self.point) is not None and self.getWidget(*self.point).getIsSelected():
                        break
                elif e.name == "right":
                    self.point[1] -= 1
                    if self.getWidget(*self.point) is not None and self.getWidget(*self.point).getIsSelected():
                        break
                elif e.name == "left":
                    self.point[1] += 1
                    if self.getWidget(*self.point) is not None and self.getWidget(*self.point).getIsSelected():
                        break
            except IndexError:
                self.point = i

    def reset(self):
        size = os.get_terminal_size()
        el_size = size.columns // self.columnsNumber
        fb = f"\033[048;2;{self.bg[0]};{self.bg[1]};{self.bg[2]}m "
        text = ""
        for i in range(0, len(self._structure_)):
            for k in range(0, len(self._structure_[i])):
                el = self.getWidget(i, k)
                if el is None:
                    elObj = None
                else:
                    if i == self.point[0] and k == self.point[1] and el.getIsSelected():
                        elObj = [
                            f"\033[038;2;{el.getHoveColor()[0]};{el.getHoveColor()[1]};{el.getHoveColor()[2]}m\033[048;2;{el.getHoveBackColor()[0]};{el.getHoveBackColor()[1]};{el.getHoveBackColor()[2]}m",
                            f"{el.getHoveText()}", "\033[0m"]
                    else:
                        elObj = [
                            f"\033[038;2;{el.getColor()[0]};{el.getColor()[1]};{el.getColor()[2]}m\033[048;2;{el.getBackColor()[0]};{el.getBackColor()[1]};{el.getBackColor()[2]}m",
                            f"{el.getText()}", "\033[0m"]
                # 对齐处理
                if elObj is None:
                    text += fb * el_size
                else:
                    if len(elObj[1]) <= el_size:
                        text += f"{elObj[0]}{elObj[1]}{elObj[2]}{fb * (el_size - len(elObj[1]))}"
                    else:
                        text += f"{elObj[0]}{elObj[1][: el_size]}{elObj[2]}"

            if (excess := size.columns % self.columnsNumber) != 0:
                text += fb * excess
            if i < len(self._structure_) - 1:
                text += "\n"

        if text != self.text:
            self.text = text
            sys.stdout.write("\033c" + text)
            sys.stdout.flush()

    def firesLoading(self):
        self.pool.submit(self._keyEvent_)
        self.reset()

    def addWidget(self, widget, row: int, column: int):
        self._structure_[row][column] = widget

    def getWidget(self, row: int, column):
        return self._structure_[row][column]

    def close(self):
        self.pool.shutdown(wait=False)
        sys.stdout.write(f"\033[?25h\033c")
