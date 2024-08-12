from tkinter import END, Tk, Frame, Text, Button, Widget, StringVar
from tkinter.ttk import Notebook
from typing import Callable


def main() -> None:

    # Only but a humble debug function, pay him no mind
    def do_nothing() -> None:
        print(":D")

    def setup() -> None:
        # This function is pretty self-explanatory... it sets up the ui
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

        def submit_faa() -> None:
            children: list[Widget] = frames["FAA"].winfo_children()
            try:
                # This is some silly JavaScript type stuff but I know the rules therefor I'm allowed to break them.
                # Seriously though this is really awful and unsafe and you want type consistency don't do this.
                # But hey it's in a try except block and you can do anything you want in those... right?
                # I just found out I can do this too... I forsee many crashed programs in my future
                text: Text = children[2]
                text.config(state="normal")
                text.delete(1.0, END)
                text.insert(1.0, faa_clearance_var.get())
                text.config(state="disabled")
            except:
                print("Error: Problem generating clearance")

        def submit_caa() -> None:
            pass

        def submit_icao() -> None:
            pass

        # These function calls create the tabs. The only thing different between them is the output when the button
        # is pressed.
        setup_mode(frames["FAA"], submit_faa)
        setup_mode(frames["CAA"], submit_caa)
        setup_mode(frames["ICAO"], submit_icao)

        return frames

    def setup_mode(frame: Frame, command: Callable) -> None:
        # This is the meat and potatoes of the whole ui and sets up the main tabs' layout
        text: Text = Text(frame, height=10, borderwidth=2)
        submit_button = Button(frame, text="Submit", command=command)
        message = Text(frame, height=10, borderwidth=2, wrap="word")
        message.insert(1.0, "test")
        message.config(state="disabled")
        frame.pack()
        text.pack(padx=10, pady=10)
        submit_button.pack()
        message.pack(padx=10, pady=10, expand=True)

    root: Tk = Tk()
    faa_clearance_var: StringVar = StringVar(root, "test2")
    caa_clearance_var: StringVar = StringVar(root, "")
    icao_clearance_var: StringVar = StringVar(root, "")
    notebook: Notebook = Notebook(root)
    setup()
    root.mainloop()


if __name__ == '__main__':
    main()
