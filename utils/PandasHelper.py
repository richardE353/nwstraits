from pandas import Series


def get_column_or_default(ds: Series, label: str, default: str = None) -> str :
    col_names = ds.index.values
    if label in col_names: return ds[label]

    if default is None: return ''
    return default

def as_string_or_default(obj, default: str = None) -> str:
    s = str(obj).strip()

    if len(s) == 0 or s.lower() == "nan":
        if default is None: return ''
        return default

    return s

def as_float_or_default(obj, default: float = float("NaN")) -> float:
    if str(obj).lower() == "nan":
        return default

    return obj
