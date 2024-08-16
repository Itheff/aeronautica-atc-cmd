import random
import traceback
from tkinter import END, Tk, Frame, Text, Button, Widget
from tkinter.ttk import Notebook
from typing import List, Literal, TextIO


# Total stack overflow tabs open concurrently: 7
# % of code ripped from ChatGPT: 0
# Don't do AI, kids.


class CSVFile:
    """Important note, this class assumes the CSV file has a header"""

    raw_csv_file: TextIO
    content: List[dict[str, str]] = []

    def __init__(self, csv_file: TextIO):
        #  I'm really proud of this code, its perfectly type safe yet wonderfully pythony
        #  (Yes I know the more pythony thing would have been to import the csv library but let me have this)
        self.raw_csv_file = csv_file
        lines: List[str] = csv_file.read().split("\n")
        headers = lines[0].split(",")
        for line in lines[1:]:
            split_line = line.split(",")
            temp_dict: dict[str, str] = {}
            for i in range(len(split_line)):
                temp_dict.update({headers[i]: split_line[i]})
            self.content.append(temp_dict)

    def find_airport(self, icao: str) -> dict[str, str]:
        try:
            for row in self.content:
                if row["ICAO"] == icao:
                    return row
            raise Exception("ICAO code does not exist or frequencies database is corrupted")
        except Exception as e:
            print(e)
            return {"ICAO": "ERROR",
                    "Name": "ERROR",
                    "DEL": "ERROR",
                    "GND": "ERROR",
                    "TWR": "ERROR",
                    "DEP": "ERROR",
                    "APP": "ERROR",
                    "CTR": "ERROR"}


class FlightPlan:

    game_call_sign: str
    radio_call_sign: str
    flight_rules: str
    aircraft_type: str
    squawk_code: str
    timestamp: str
    requested_flight_level: str
    departure: str
    arrival: str
    route: str
    remarks: str
    frequencies: CSVFile
    #  Can you tell I'm used to Java?

    def __init__(self, raw_flight_plan: str):

        #  This removes a bunch of unnecessary characters from the flight plan
        raw_flight_plan = raw_flight_plan
        raw_flight_plan = raw_flight_plan.replace("\"", "\t")
        raw_flight_plan = raw_flight_plan.replace("/", "\t")
        raw_flight_plan = raw_flight_plan.replace(" ", "")
        raw_flight_plan = raw_flight_plan.replace("\n", "\t")
        split_flight_plan = raw_flight_plan.split("\t")

        # This mess is to remove empty list items without crashing. I don't know of a better way to do this.
        to_remove: List[int] = []
        for i in range(len(split_flight_plan)):
            if split_flight_plan[i] == "\t" or split_flight_plan[i] == "":
                to_remove.append(i)
        to_remove.reverse()
        for i in to_remove:
            split_flight_plan.pop(i)

        #  This makes sure that the potentially empty first element is always present for consistent list ordering
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

        self.game_call_sign = split_flight_plan[1].upper()
        self.radio_call_sign = split_flight_plan[2].upper()
        self.flight_rules = split_flight_plan[3].upper()
        self.aircraft_type = split_flight_plan[4].upper()
        self.generate_squawk()
        self.timestamp = split_flight_plan[6].upper()
        self.requested_flight_level = split_flight_plan[7].upper()
        self.departure = split_flight_plan[8].upper()
        self.arrival = split_flight_plan[9].upper()
        self.route = split_flight_plan[10].upper()
        self.remarks = split_flight_plan[11].upper()
        self.frequencies = CSVFile(open("resources/frequencies_database.csv", "r"))

    def generate_squawk(self) -> None:
        temp = ""
        while len(temp) >= 4:
            temp += str(random.randint(0, 7))
        self.squawk_code = temp

    def find_frequency(self, airport: str, frequency_type: Literal["del", "gnd", "twr", "app", "dep", "ctr"]) -> str:
        airport_dict: dict[str, str] = self.frequencies.find_airport(airport)
        return airport_dict[frequency_type.upper()]

    def to_string(self, phraseology: Literal["faa", "caa", "icao"]) -> str:
        match phraseology:
            case "faa":
                return_string: str = (f"CLR {self.radio_call_sign} TO ARR {self.arrival} VIA {self.route}. RMK INITIAL "
                                      f"ALT 4000 EXPECT {self.requested_flight_level} 10 MINS AFT DEP. DEP FREQ ON "
                                      f"{self.find_frequency(self.departure, 'dep')} SQUAWK {self.squawk_code}. "
                                      f"CTC GND ON {self.find_frequency(self.departure, 'gnd')} FOR PUSH AND TAXI.")
                return return_string
            case "caa":
                return "NOT IMPLEMENTED"  # TODO IMPLEMENT THIS
            case "icao":
                return "NOT IMPLEMENTED"  # TODO IMPLEMENT THIS


class PDCFrame(Frame):

    flight_plan_input: Text
    submit_button: Button
    pdc_output: Text
    phraseology: Literal["faa", "caa", "icao"]

    def __init__(self, master: Widget, phraseology: Literal["faa", "caa", "icao"]):
        super().__init__(master)
        self.phraseology = phraseology
        self.flight_plan_input: Text = Text(self, height=10, borderwidth=2)
        self.submit_button = Button(self, text="Submit", command=self.submit)
        self.pdc_output = Text(self, height=10, borderwidth=2, wrap="word")
        self.pdc_output.config(state="disabled")
        self.pack()
        self.flight_plan_input.pack(padx=10, pady=10)
        self.submit_button.pack()
        self.pdc_output.pack(padx=10, pady=10, expand=True)

    def submit(self):
        try:
            self.pdc_output.config(state="normal")
            self.pdc_output.delete("1.0", END)
            flight_plan = FlightPlan(self.flight_plan_input.get("1.0", END))
            self.pdc_output.insert(1.0, flight_plan.to_string(self.phraseology))
            self.pdc_output.config(state="disabled")
        except Exception as e:
            traceback.print_tb(e.__traceback__)


class App(Tk):

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
        icao_frame = PDCFrame(notebook, "icao")
        notebook.add(faa_frame, text="FAA")
        notebook.add(caa_frame, text="CAA")
        notebook.add(icao_frame, text="ICAO")
        notebook.pack()


def main() -> None:
    root: App = App()
    root.mainloop()


if __name__ == '__main__':
    main()
