from colorama import Fore, Style, init


def colorama_init(func):
    def wrapper(*args, **kwargs):
        init()
        return func(*args, **kwargs)

    return wrapper


class ColorPrinter:
    COLORS = {
        'BLACK': Fore.BLACK,
        'RED': Fore.RED,
        'GREEN': Fore.GREEN,
        'YELLOW': Fore.YELLOW,
        'BLUE': Fore.BLUE,
        'MAGENTA': Fore.MAGENTA,
        'CYAN': Fore.CYAN,
        'WHITE': Fore.WHITE
    }

    @colorama_init
    def __init__(self):
        pass

    def print_color(self, prefix, variable, color, bold=False):
        if color in self.COLORS:
            if bold:
                print(self.COLORS[color] + Style.BRIGHT + prefix + str(variable) + Style.RESET_ALL)
            else:
                print(self.COLORS[color] + prefix + str(variable) + Style.RESET_ALL)
        else:
            print("Invalid color")

# # 使用示例
# printer = ColorPrinter()
# printer.print_color("这是红色的文字", "RED", True)
# printer.print_color("这是绿色的文字", "GREEN")
# printer.print_color("这是蓝色的文字", "BLUE")
# printer.print_color("这是黄色的文字", "YELLOW")


# from colorama import Fore, Back, Style, init

# # 初始化 colorama
# init()

# print(Fore.RED + "这是红色的文字" + Fore.RESET)
# print(Fore.GREEN + "这是绿色的文字" + Fore.RESET)
# print(Fore.BLUE + Style.BRIGHT + "这是蓝色和加粗的文字" + Style.RESET_ALL)
# print(Fore.YELLOW + Back.BLACK + "这是黄色和下划线的文字" + Style.RESET_ALL)


# from termcolor import colored

# print(colored("这是红色的文字", "red"))
# print(colored("这是绿色的文字", "green"))
# print(colored("这是蓝色和加粗的文字", "blue", attrs=["bold"]))
# print(colored("这是黄色和下划线的文字", "yellow", attrs=["underline"]))
