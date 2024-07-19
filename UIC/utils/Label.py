from UIC.module.craft.template import template


class Label(template):
    def __init__(self, text: str):
        super().__init__(text)
        super()._setIsSelected_(False)
