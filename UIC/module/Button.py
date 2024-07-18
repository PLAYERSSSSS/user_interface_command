from UIC.module.craft.template import template


class Button(template):
    def __init__(self, text: str, press=None):
        super().__init__(text)
        if press is not None:
            self.press = press

    def press(self):
        pass
