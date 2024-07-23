import re

import keyboard
from keyboard import KEY_DOWN

from UIC.module.craft.template import template
from UIC.utils.mappingTable import caseMappingTable


class Input(template):
    def __init__(self, head: str = "", value: str = "", changeEvent=lambda event: None, pressEvent=lambda: None):
        super().__init__(head + value)
        self.value = value
        self.head = head
        self.isSelectInput = False
        self.changeEvent = changeEvent
        self.pressEvent = pressEvent

    def getValue(self):
        return self.value

    def setText(self, text: str):
        self.value = text
        self._text_ = self.head + self.value

    def getHoveText(self):
        return self._text_

    def press(self):
        self.pressEvent()

    def change(self, e: keyboard.KeyboardEvent):
        self.changeEvent(e)
        if len(e.name) > 1:
            if e.name == "space":
                self.setText(self.value + " ")

            if e.name == "tab":
                self.setText(self.value + "    ")

        else:
            if "shift" in e.modifiers:
                if re.match("[a-z]", e.name):
                    self.setText(self.value + e.name.upper())
                else:
                    self.setText(self.value + caseMappingTable.get(e.name))
            else:
                self.setText(self.value + e.name)
