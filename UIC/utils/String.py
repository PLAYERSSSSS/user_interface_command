class String:
    def __init__(self, text: str):
        self.text = text
        self.len = len(text)

    def setLen(self, v: int):
        self.len = v

    def __len__(self):
        return self.len

    def __str__(self):
        return self.text

    def __getitem__(self, item):
        pass
