import datetime

VERSION=({{ version.major }}, {{ version.minor }}, {{ version.patch }})
COMPILATION_DATE = datetime.datetime.fromtimestamp({{ compile_timestamp }})