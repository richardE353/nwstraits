import os
from dataclasses import dataclass
from io import StringIO
from math import isnan

from models.KelpDataRow import KelpSurvey


@dataclass
class KelpDataLog:
    params: list
    target: str
    kelp_data: dict

    # https://stackoverflow.com/questions/19926089/python-equivalent-of-java-stringbuffer
    str_buffer: StringIO = StringIO()

    def log_records_filtered_by(self, title: str, filter_func):
        self.str_buffer.write("\n\n" + title + "\n")

        for county in self.kelp_data.keys():
            surveys = list(filter(filter_func, self.kelp_data[county]))

            if surveys:
                self.str_buffer.write("\t" + county + "\n")
            for s in surveys:
                self.str_buffer.write("\t\t" + s.file_prefix() + "\n")

    def append_parameter_info(self):
        self.str_buffer.write("Runtime parameters\n")
        for k, v in self.params:
            self.str_buffer.write("\t" + k + ": " + v + "\n")

    def append_missing_data_sheets(self):
        def data_sheets_missing(s: KelpSurvey) -> bool:
            return len(s.data_file_names.data_sheet_1) + len(s.data_file_names.data_sheet_2) == 0

        self.log_records_filtered_by("Surveys Missing DataSheet files:", data_sheets_missing)

    def append_missing_gpx_files(self):
        def gpx_files_missing(s: KelpSurvey) -> bool:
            return len(s.data_file_names.track_gps_file) == 0

        self.log_records_filtered_by("Surveys Missing Track GPX files:", gpx_files_missing)

    def append_missing_depths_data(self):
        def shore_depth_missing(s: KelpSurvey) -> bool:
            return isnan(s.depth_1_at_shore_edge) and isnan(s.depth_2_at_shore_edge)

        def outer_edge_depth_missing(s: KelpSurvey) -> bool:
            return isnan(s.depth_1_at_outer_edge) and isnan(s.depth_2_at_outer_edge)

        self.log_records_filtered_by("Surveys Missing Shore Depth Measurements:", shore_depth_missing)
        self.log_records_filtered_by("Surveys Missing Outer Edge Depth Measurements:", outer_edge_depth_missing)

    def append_missing_temps_data(self):
        def shore_temp_missing(s: KelpSurvey) -> bool:
            return isnan(s.temp_1_at_shore_edge) and isnan(s.temp_2_at_shore_edge)

        def outer_edge_temp_missing(s: KelpSurvey) -> bool:
            return isnan(s.temp_1_at_outer_edge) and isnan(s.temp_2_at_outer_edge)

        self.log_records_filtered_by("Surveys Missing Shore Temp Measurements:", shore_temp_missing)
        self.log_records_filtered_by("Surveys Missing Outer Edge Temp Measurements:", outer_edge_temp_missing)

    def append_missing_tidal_corrections(self):
        def missing_tidal_correction(s: KelpSurvey) -> bool: return s.noaa_data_missing()

        self.log_records_filtered_by("Surveys with missing NOAA adjustment data:", missing_tidal_correction)

    def append_cluster_info(self):
        def kelp_clusters(s: KelpSurvey) -> list: return s.kelp_clusters

        self.log_records_filtered_by("Surveys with kelp cluster info:", kelp_clusters)

    def append_survey_info(self):
        self.str_buffer.write("\n\nSurveys By County:\n")

        for county in self.kelp_data.keys():
            self.str_buffer.write("\t" + county + "\n")

            for s in self.kelp_data[county]:
                self.str_buffer.write("\t\t" + s.location + " " + s.survey_date.replace("-", "_") + "\n")

    def append_volunteer_info(self):
        def has_volunteer_names(ks: KelpSurvey) -> bool:
            return len(ks.volunteer_info.names) > 0

        self.str_buffer.write("\n\nSurvey Volunteers:\n")

        for county in self.kelp_data.keys():
            surveys = list(filter(has_volunteer_names, self.kelp_data[county]))

            if surveys:
                self.str_buffer.write("\t" + county + "\n")

            for s in surveys:
                self.str_buffer.write("\t\t" + s.file_prefix() + " " + s.volunteer_info.names + "\n")

    def write_log(self, target: str):
        f = open(target, 'w', encoding="utf-8")
        f.write(self.str_buffer.getvalue())
        f.close()

    def create_and_write_log(self, year: int):
        self.append_parameter_info()
        self.append_missing_data_sheets()
        self.append_missing_gpx_files()
        self.append_missing_depths_data()
        self.append_missing_temps_data()
        self.append_missing_tidal_corrections()
        self.append_cluster_info()
        self.append_survey_info()
        self.append_volunteer_info()

        fn = 'extractionLog' + str(year) + '.txt'
        full_path = os.path.join(self.target, fn)
        self.write_log(full_path)
