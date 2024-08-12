from tkinter import END, Tk, Frame, Text, Button, Widget
from tkinter.ttk import Notebook
from typing import Callable, List


# Total stack overflow tabs open concurrently: 7
# % of code ripped from ChatGPT: 0
# Don't do AI, kids.


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

        def split_flight_plan(flight_plan: str) -> List[str]:
            # This function is quite verbose and could likely be done better... but I'm not going to.
            # All you need to know is that it removes unnecessary characters and splits the string into a list.
            flight_plan = flight_plan.replace("\"", "\t")
            flight_plan = flight_plan.replace("/", "\t")
            flight_plan = flight_plan.replace(" ", "")
            flight_plan = flight_plan.replace("\n", "\t")
            local_split_flight_plan = flight_plan.split("\t")
            # This mess is to remove empty list items without crashing. I don't know of a better way to do this.
            to_remove: List[int] = []
            for i in range(len(local_split_flight_plan)):
                if local_split_flight_plan[i] == "\t" or local_split_flight_plan[i] == "":
                    to_remove.append(i)
            to_remove.reverse()
            for i in to_remove:
                local_split_flight_plan.pop(i)
            return local_split_flight_plan

        def submit_faa() -> None:

            def generate_faa_clearance(flight_plan: str) -> str:
                local_split_flight_plan: List[str] = split_flight_plan(flight_plan)
                match local_split_flight_plan[0]:
                    case "DEPARTURE":
                        pass
                    case "ARRIVAL":
                        pass
                    case "ENROUTE":
                        pass
                    case "EMERGENCY":
                        pass
                    case _:
                        local_split_flight_plan.insert(0, "")
                print(local_split_flight_plan)
                return "Flight plan received"  # TODO Bring it all together here, its late and I'm going to bed

            children: list[Widget] = frames["FAA"].winfo_children()
            try:
                # This is some silly JavaScript type stuff but I know the rules therefor I'm allowed to break them.
                # Seriously though this is really awful and unsafe and you want type consistency don't do this.
                # But hey it's in a try except block and you can do anything you want in those... right?
                # I just found out I can do this too... I forsee many crashed programs in my future
                text: Text = children[2]  # Pyright really hates this and I kinda do too, oh well.
                text.config(state="normal")
                text.delete(1.0, END)
                input_field: Text = children[0]  # This too.
                text.insert(1.0, generate_faa_clearance(input_field.get("1.0", END)))  # I love one-liners.
                text.config(state="disabled")
            except Exception as e:
                print("Error: Problem generating clearance")
                print(e)

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
    notebook: Notebook = Notebook(root)
    setup()
    root.mainloop()


if __name__ == '__main__':
    main()
