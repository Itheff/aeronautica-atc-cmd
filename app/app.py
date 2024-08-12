from tkinter import StringVar, Tk, Frame, Text, Button, Message
from tkinter.ttk import Notebook


def main() -> None:

    def setup() -> None:
        root.geometry('512x512')
        root.resizable(False, False)
        root.title("Aeronautica ATC")
        frames: dict[str, Frame] = setup_frames()
        for key in frames.keys():
            notebook.add(frames[key], text=key)
        notebook.pack(fill='both')

    def setup_frames() -> dict[str, Frame]:
        # Inserting the frames into a dictionary allows using a loop in the setup function above
        frames: dict[str, Frame] = {
            "FAA": Frame(notebook),
            "CAA": Frame(notebook),
            "ICAO": Frame(notebook)}
        setup_faa(frames["FAA"])
        setup_caa(frames["CAA"])
        setup_icao(frames["ICAO"])
        return frames

    def setup_faa(frame: Frame) -> None:

        text: Text = Text(frame, height=10, borderwidth=2)
        submit_button = Button(frame, text="Submit")
        message = Text(frame, height=10, borderwidth=2, wrap="word")
        message.insert(1.0, "test")
        message.config(state="disabled")
        frame.pack()
        text.pack(padx=10, pady=10)
        submit_button.pack()
        message.pack(padx=10, pady=10, expand=True)

    def setup_caa(frame: Frame) -> None:
        pass  # TODO put main functions of app here

    def setup_icao(frame: Frame) -> None:
        pass  # TODO put main functions of app here

    root: Tk = Tk()
    notebook: Notebook = Notebook(root)
    setup()
    root.mainloop()


if __name__ == '__main__':
    main()
