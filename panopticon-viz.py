#! /usr/bin/env python3
import pandas as pd
import plotly.express as px
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input-file", type=str, help="csv file exported from Panopticon"
    )
    args = vars(parser.parse_args())

    df = pd.read_csv(args["input-file"])
    df = df[df.activity != "none"]
    fig = px.pie(
        df, values="milliseconds", names="activity", title="Panopticon Time Chart"
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.show()
