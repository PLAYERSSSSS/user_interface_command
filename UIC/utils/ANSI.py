

def getRGB_ANSI_String_back(color: (int, int, int)) -> str:
    return f"\033[038;2{color[0]};{color[1]};{color[2]}m"
