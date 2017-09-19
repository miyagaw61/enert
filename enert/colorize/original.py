from toplevel import *

def inf(strings, color="green"):
    term_y, term_x = get_term_size()
    if color == "green":
        print(green("\n" + "="*term_x, "bold"))
        print("[" + red("+", "bold") + "]" + strings)
        print(green("="*term_x + "\n", "bold"))
    if color == "red":
        print(red("\n" + "="*term_x, "bold"))
        print("[" + red("+", "bold") + "]" + strings)
        print(red("="*term_x + "\n", "bold"))
    if color == "blue":
        print(blue("\n" + "="*term_x, "bold"))
        print("[" + red("+", "bold") + "]" + strings)
        print(blue("="*term_x + "\n", "bold"))

