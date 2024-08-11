from tkinter import Tk
from tkinter.ttk import Notebook, Frame


def main() -> None:
    root: Tk = Tk()
    notebook: Notebook = Notebook(root)
    setup(root, notebook)
    root.mainloop()


def setup(root: Tk, notebook: Notebook) -> None:
    root.geometry('512x512')
    root.resizable(False, False)
    root.title("Aeronautica ATC")
    setup_frames()
    notebook.pack(fill='both', expand=True)


def setup_frames() -> dict[str, Frame]:
    frames: dict[str, Frame] = {
        "faa": Frame(),
        "caa": Frame(),
        "icao": Frame()}
    setup_faa(frames["faa"])
    setup_caa(frames["caa"])
    setup_icao(frames["icao"])
    return frames


def setup_faa(frame: Frame):
    pass  # TODO put main functions of app here


def setup_caa(frame: Frame):
    pass  # TODO put main functions of app here


def setup_icao(frame: Frame):
    pass  # TODO put main functions of app here


if __name__ == '__main__':
    main()
