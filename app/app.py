import random
import traceback
from tkinter import END, Tk, Frame, Text, Button, Widget
from tkinter.ttk import Notebook
from typing import List, Literal


class PDCBuilder:
    """
    The PDCBuilder class is primarily meant to ensure the frequencies database is read only once at the beginning of the
    program instead of every time a PDC is generated. It does not store the flight plans from PDC's it generates.
    """
    airports: List[dict[str, str]] = []

    def read_database(self) -> None:
        """
        This method runs once at the beginning of the program when this object is instantiated. It read the contents of
        the frequencies database and stores those contents in the airports list. Each airport is represented as a
        dictionary.
        """
        raw_csv_file = open("resources/frequencies_database.csv", "r")
        lines: List[str] = raw_csv_file.read().split("\n")
        headers = lines[0].split(",")
        for line in lines[1:]:
            split_line = line.split(",")
            temp_dict: dict[str, str] = {}
            for i in range(len(split_line)):
                temp_dict.update({headers[i]: split_line[i]})
            self.airports.append(temp_dict)

    @staticmethod
    def generate_squawk() -> str:
        """
        This method generates a 4 digit octal number representing a squawk code and returns it as a string.
        """
        squawk = ""
        while len(squawk) < 4:
            squawk += str(random.randint(0, 7))
        return squawk

    @staticmethod
    def split_flight_plan(flight_plan: str) -> List[str]:
        """
        This method takes a string of a flight plan and returns a list of its component parts while removing all unused
        characters. It also ensures there is a consistent number of items in the list.
        """
        flight_plan = flight_plan.replace("\"", "\t")
        flight_plan = flight_plan.replace("/", "\t")
        flight_plan = flight_plan.replace(" ", "")
        flight_plan = flight_plan.replace("\n", "\t")
        split_flight_plan = flight_plan.split("\t")
        to_remove: List[int] = []
        for i in range(len(split_flight_plan)):
            if split_flight_plan[i] == "\t" or split_flight_plan[i] == "":
                to_remove.append(i)
        to_remove.reverse()
        for i in to_remove:
            split_flight_plan.pop(i)

        match split_flight_plan[0]:
            case "DEPARTURE":
                pass
            case "ARRIVAL":
                pass
            case "ENROUTE":
                pass
            case "EMERGENCY":
                pass
            case _:
                split_flight_plan.insert(0, "")
        return split_flight_plan

    def find_frequency(self, icao: str, frequency_type: Literal["del", "gnd", "twr", "app", "dep", "ctr"]) -> str:
        """
        This method searches the database and finds the airport matching the ICAO code given, and then queries the
        airport dictionary for the type of frequencies requested.
        """
        airport: dict[str, str] = {}
        for row in self.airports:
            if row["ICAO"] == icao:
                airport = row
                break
            airport = {"ICAO": "ERROR",
                       "Name": "ERROR",
                       "DEL": "ERROR",
                       "GND": "ERROR",
                       "TWR": "ERROR",
                       "DEP": "ERROR",
                       "APP": "ERROR",
                       "CTR": "ERROR"}
        return airport[frequency_type.upper()]

    def build_pdc(self, flight_plan: str, phraseology: Literal["faa", "caa", "icao"]) -> str:
        """
        This method brings everything together and returns the completed PDC. You only need to call this method to
        generate the PDC, everything else is done automatically by this method.
        """
        split_flight_plan: List[str] = self.split_flight_plan(flight_plan)
        match phraseology:
            case "faa":
                return_string: str = (f"CLR {split_flight_plan[2].upper()} TO ARR "
                                      f"{split_flight_plan[9].upper()} VIA "
                                      f"{split_flight_plan[10].upper()}. RMK INITIAL ALT 4000 EXPECT "
                                      f"{split_flight_plan[7]} 10 MINS AFT DEP. DEP FREQ ON "
                                      f"{self.find_frequency(split_flight_plan[8], 'gnd')} SQUAWK "
                                      f"{self.generate_squawk()}. CTC GND ON "
                                      f"{self.find_frequency(split_flight_plan[8], 'dep')} FOR PUSH AND TAXI.")
                return return_string
            case "caa":
                return_string: str = (f"{split_flight_plan[2].upper()} CLR TO ARR {split_flight_plan[9].upper()} VIA "
                                      f"{split_flight_plan[10].upper()}. SQUAWK {self.generate_squawk()}, ATIS A. "
                                      f"WHEN READY CALL FREQ {self.find_frequency(split_flight_plan[8], 'gnd')}.")
                return return_string
            case "icao":
                return "NOT IMPLEMENTED"  # TODO IMPLEMENT THIS

    def __init__(self):
        self.read_database()


class PDCFrame(Frame):
    """
    The PDCFrame class is the main component of the UI and is the content seen in the 3 tabs.
    """
    flight_plan_input: Text
    submit_button: Button
    pdc_output: Text
    phraseology: Literal["faa", "caa", "icao"]
    pdc_builder: PDCBuilder

    def __init__(self, master: Widget, phraseology: Literal["faa", "caa", "icao"]):
        super().__init__(master)
        self.phraseology = phraseology
        self.pdc_builder = PDCBuilder()
        self.flight_plan_input: Text = Text(self, height=10, borderwidth=2)
        self.submit_button = Button(self, text="Submit", command=self.submit)
        self.pdc_output = Text(self, height=10, borderwidth=2, wrap="word")
        self.pdc_output.config(state="disabled")
        self.pack()
        self.flight_plan_input.pack(padx=10, pady=10)
        self.submit_button.pack()
        self.pdc_output.pack(padx=10, pady=10, expand=True)

    def submit(self):
        """
        The submit method is called every time the submit button is pressed. It generates a PDC from the PDCBuilder and
        outputs it to the pdc_output.
        :return:
        """
        try:
            self.pdc_output.config(state="normal")
            self.pdc_output.delete("1.0", END)
            self.pdc_output.insert(1.0, self.pdc_builder.build_pdc(self.flight_plan_input.get("1.0", END),
                                                                   self.phraseology))
            self.pdc_output.config(state="disabled")
        except Exception as e:
            traceback.print_tb(e.__traceback__)


class App(Tk):
    """
    The App class is the root component of the UI and contains the notebook which then contains the 3 tabs. It is mostly
    a basic Tk class but with extra steps added to the __init__ to create the unique UI of the program.
    """
    notebook: Notebook
    faa_frame: Frame
    caa_frame: Frame
    icao_frame: Frame

    def __init__(self):
        super().__init__()
        self.geometry("512x512")
        self.resizable(False, False)
        self.title("Aeronautica ATC")
        notebook = Notebook(self)
        faa_frame = PDCFrame(notebook, "faa")
        caa_frame = PDCFrame(notebook, "caa")
        caa_frame.pdc_output.config(state="normal")
        caa_frame.pdc_output.insert(END, "Disclaimer, you must set the correct ATIS every time a PDC is generated")
        caa_frame.pdc_output.config(state="disabled")
        icao_frame = PDCFrame(notebook, "icao")
        icao_frame.flight_plan_input.insert(END, "INOP")
        icao_frame.flight_plan_input.config(state="disabled", background="gray75")
        icao_frame.pdc_output.config(state="disabled", background="gray75")
        notebook.add(faa_frame, text="FAA")
        notebook.add(caa_frame, text="CAA")
        notebook.add(icao_frame, text="ICAO")
        notebook.pack()


def main() -> None:
    """
    This function holds the root of the program and runs the main loop of the window
    """
    root: App = App()
    root.mainloop()


if __name__ == '__main__':
    main()
