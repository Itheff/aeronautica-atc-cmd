import tkinter as tk


def main() -> None:
    root: tk.Tk = tk.Tk()
    setup(root)


def setup(root: tk.Tk) -> None:
    root.geometry('512x512')
    root.resizable(False, False)
    root.title("Aeronautica ATC")


if __name__ == '__main__':
    main()
