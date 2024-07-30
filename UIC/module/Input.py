import re
import sys
from typing import Literal

import keyboard

from UIC.module.craft.template import template
from UIC.utils.mappingTable import caseMappingTable


class Input(template):
    def __init__(self, head: str = "", value: str = "", type: Literal["text", "password", "numeral"] = "text",
                 changeEvent=lambda event: None,
                 pressEvent=lambda: None):
        super().__init__(head + value)
        self.type = type
        self.value = value
        self.head = head
        self.isSelectInput = False
        self.changeEvent = changeEvent
        self.pressEvent = pressEvent

    def getValue(self):
        return self.value

    def setValue(self, v):
        self.value = v

    def setText(self, text: str):
        self.value = text
        self._text_ = self.head + self.value

    def getHoveText(self):
        return self._text_

    def keyEvent(self, e, frame):
        if len(e.name) == 1 or e.name in ["space", "tab"]:
            self.change(e)
        else:
            if e.name == "enter":
                self.press()
            if e.name == "backspace":
                self.setValue(self.value[0: -1])
                if self.type == "text":
                    self.setText(self.getValue())
                elif self.type == "password":
                    self.setText(len(self.getValue()) * "*")
                elif self.type == "numeral":
                    self.setText(self.getValue())
        frame.reset()
        return True

    def press(self):
        self.pressEvent()

    def change(self, e: keyboard.KeyboardEvent):
        self.changeEvent(e)
        if self.type == "text":
            if len(e.name) > 1:
                if e.name == "space":
                    self.setText(self.getValue() + " ")

                if e.name == "tab":
                    self.setText(self.getValue() + "    ")

            else:
                if keyboard.is_pressed("shift"):
                    if sys.platform.startswith('linux'):
                        if re.match("[a-z]", e.name):
                            self.setText(self.getValue() + e.name.upper())
                        else:
                            self.setText(self.getValue() + caseMappingTable.get(e.name))
                    else:
                        self.setText(self.getValue() + e.name)
                else:
                    self.setText(self.getValue() + e.name)
        elif self.type == "password":
            if len(e.name) == 1:
                if keyboard.is_pressed("shift"):
                    if sys.platform.startswith('linux'):
                        if re.match("[a-z]", e.name):
                            self.setValue(self.getValue() + e.name.upper())
                        else:
                            self.setValue(self.getValue() + caseMappingTable.get(e.name))
                    else:
                        self.setValue(self.getValue() + e.name)
                else:
                    self.setValue(self.getValue() + e.name)

                self._text_ = self.head + len(self.getValue()) * "*"
        elif self.type == "numeral":
            if len(e.name) == 1 and re.match("[0-9]|[-+.]", e.name):
                if len(self.getValue()) == 0 and re.match("[-+]", e.name):
                    self.setText(self.getValue() + e.name)
                elif len(self.getValue()) > 0 and self.getValue().rfind(".") == -1 and e.name == ".":
                    self.setText(self.getValue() + e.name)
                elif re.match("[0-9]", e.name):
                    self.setText(self.getValue() + e.name)
