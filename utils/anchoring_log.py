from dataclasses import dataclass

from models.anchor_row import AnchoringSurvey
from io import StringIO
import os


@dataclass()
class AnchoringLog:
    params: list
    target: str
    anchoring_data: dict

    # https://stackoverflow.com/questions/19926089/python-equivalent-of-java-stringbuffer
    str_buffer: StringIO = StringIO()

    def write_log(self, target: str):
        f = open(target, 'w', encoding="utf-8")
        f.write(self.str_buffer.getvalue())
        f.close()

    def append_parameter_info(self):
        self.str_buffer.write("Runtime parameters\n")
        for k, v in self.params:
            self.str_buffer.write("\t" + k + ": " + v + "\n")

    def append_surveys_by_county(self):
        self.str_buffer.write("\n\nSurveys By County:\n")

        for county in self.anchoring_data.keys():
            self.str_buffer.write("\t" + county + "\n")

            for s in self.anchoring_data[county]:
                (self.str_buffer.
                 write("\t\t" + s.survey_info() + "\n"))

    def append_observer_info(self):
        self.str_buffer.write("\n\nSurvey Volunteers:\n")

        def has_observers(r: AnchoringSurvey) -> bool:
            return len(r.observer_names) > 0

        for county in self.anchoring_data.keys():
            surveys = list(filter(has_observers, self.anchoring_data[county]))

            if surveys:
                self.str_buffer.write("\t" + county + "\n")

            for s in surveys:
                self.str_buffer.write("\t\t" + s.file_prefix() + " " + s.observer_names + "\n")

    def create_and_write_log(self, year: int):
        self.append_parameter_info()
        self.append_surveys_by_county()
        self.append_observer_info()

        fn = 'extractionLog' + str(year) + '.txt'
        full_path = os.path.join(self.target, fn)
        self.write_log(full_path)
