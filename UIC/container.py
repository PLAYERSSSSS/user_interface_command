import os
import sys
import time
from concurrent.futures.thread import ThreadPoolExecutor

import keyboard
from blessings import Terminal

from UIC.module.Input import Input
from UIC.module.Button import Button


class Frame:
    def __init__(self, lineNumber: int, columnsNumber: int, threadingPool=ThreadPoolExecutor(max_workers=1),
                 vacancyReplacement: str = ""):
        self.isLinux = sys.platform.startswith('linux')
        self.vacancyReplacement = vacancyReplacement
        self.pool = threadingPool
        self.point = [0, 0]
        self.lineNumber = lineNumber
        self.columnsNumber = columnsNumber
        self._structure_ = []
        self._newStructure_(lineNumber, columnsNumber)
        self.term = Terminal()
        if not self.isLinux:
            os.system("")

    def _newStructure_(self, lineNumber: int, columnsNumber: int):
        self._structure_ = [[None] * columnsNumber for _ in range(lineNumber)]

    def _keyEvent_(self):
        def callback(e: keyboard.KeyboardEvent):
            el = self.getWidget(*self.point)
            if el is not None and isinstance(el, Input):
                if len(e.name) == 1 or e.name in ["space", "tab"]:
                    el.change(e)
                else:
                    if e.name == "enter":
                        el.press()
                    if e.name == "backspace":
                        el.setText(el.value[0: -1])
                self.reset()

            if e.event_type == 'down':
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
                    if isinstance(element, Button):
                        element.press()

                self.reset()

        keyboard.on_press(callback, suppress=True)
        keyboard.wait()

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
        print("\033c", end="")
        text = ""
        for i in range(0, len(self._structure_)):
            for k in range(0, len(self._structure_[i])):
                el = self.getWidget(i, k)
                if el is None:
                    text += self.vacancyReplacement
                    continue
                if i == self.point[0] and k == self.point[1] and el.getIsSelected():
                    text += f"\033[038;2;{el.getHoveColor()[0]};{el.getHoveColor()[1]};{el.getHoveColor()[2]}m\033[048;2;{el.getHoveBackColor()[0]};{el.getHoveBackColor()[1]};{el.getHoveBackColor()[2]}m{el.getHoveText()}\033[0m"
                else:
                    text += f"\033[038;2;{el.getColor()[0]};{el.getColor()[1]};{el.getColor()[2]}m\033[048;2;{el.getBackColor()[0]};{el.getBackColor()[1]};{el.getBackColor()[2]}m{el.getText()}\033[0m"
            text += "\n"
        print(text)

    def firesLoading(self):
        self.pool.submit(self._keyEvent_)
        self.reset()

    def addWidget(self, widget, row: int, column: int):
        self._structure_[row][column] = widget

    def getWidget(self, row: int, column):
        return self._structure_[row][column]

    def close(self):
        self.pool.shutdown(wait=False)
        print("\033c")
