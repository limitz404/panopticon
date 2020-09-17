#! /usr/bin/env python3
import argparse
import csv
from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px

import storage


def get_durations(begin, end):
    """Return the relative path to a CSV file containing the activity duration
    intervals between the specified dates. The datetimes of the rows of the
    CSV will be >= begin and <= end.
    """
    # Get the minimum and maximum datetimes from the database. These will be the
    # "infinity" values used in the name of the file (if one or both of
    # `begin`/`end` is `None`). This is helpful, so that the names of the
    # files always indicate the truth about what they contain.
    least, most = storage.select_maximal_time_range()

    # If there are no rows, then `least == most == None`, and we can return a
    # special no-rows CSV.
    if least is None:
        assert most is None
        return []

    return storage.select_durations(begin, end)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--start-time",
        type=str,
        default="2000-01-01T00:00",
        help="select durations after the specified time in ISO format. Example: 2020-01-01T00:00-04:00",
    )
    parser.add_argument(
        "-e",
        "--end-time",
        type=str,
        default=datetime.now().isoformat(),
        help="select durations before the specified time in ISO format. Example: 2020-01-01T00:00-04:00",
    )

    args = parser.parse_args()

    df = pd.DataFrame(
        get_durations(
            datetime.fromisoformat(args.start_time),
            datetime.fromisoformat(args.end_time),
        ),
        columns=["begin", "end", "activity", "milliseconds"],
    )

    df = df[df.activity != "none"]
    fig = px.pie(
        df,
        values="milliseconds",
        names="activity",
        title="Panopticon Time Chart",
        template="plotly_dark",
    )

    fig.update_traces(textposition="outside", textinfo="percent+label")
    fig.show()
