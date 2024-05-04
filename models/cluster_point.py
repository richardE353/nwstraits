from dataclasses import dataclass

from pandas import Series

import utils.pandas_helper as ph


@dataclass(frozen=True)
class KelpClusterPoint:
    gps_point_name: str
    depth: float
    water_temp: float
    observations: str


def extract_kelp_clusters(ds: Series) -> list:
    clusters = list()

    for i in range(1, 4):
        index_suffix = str(i)
        cluster_info = KelpClusterPoint(
            ph.as_string_or_default(ds["kc_gps_point_name" + index_suffix]),
            ph.as_float_or_default(ds["kc_depth" + index_suffix]),
            ph.as_float_or_default(ds["kc_temp" + index_suffix]),
            ph.as_string_or_default(ds["kc_observation" + index_suffix])
        )
        if len(cluster_info.gps_point_name) > 0: clusters.append(cluster_info)

    return clusters
