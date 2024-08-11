from tkinter import Tk, Frame
from tkinter.ttk import Notebook


def main() -> None:
    root: Tk = Tk()
    notebook: Notebook = Notebook(root)
    setup(root, notebook)
    root.mainloop()


def setup(root: Tk, notebook: Notebook) -> None:
    root.geometry('512x512')
    root.resizable(False, False)
    root.title("Aeronautica ATC")
    frames: dict[str, Frame] = setup_frames()
    for key in frames.keys():
        notebook.add(frames[key], text=key)
    notebook.pack(fill='both')


def setup_frames() -> dict[str, Frame]:
    frames: dict[str, Frame] = {
        "FAA": Frame(),
        "CAA": Frame(),
        "ICAO": Frame()}
    setup_faa(frames["FAA"])
    setup_caa(frames["CAA"])
    setup_icao(frames["ICAO"])
    return frames


def setup_faa(frame: Frame) -> None:
    pass  # TODO put main functions of app here


def setup_caa(frame: Frame) -> None:
    pass  # TODO put main functions of app here


def setup_icao(frame: Frame) -> None:
    pass  # TODO put main functions of app here


if __name__ == '__main__':
    main()
