import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def group_df_by_hour(df, column="timestamp"):
    grouped_by_hour = (
        pd.to_datetime(df[column])
        .dt.floor("H")
        .value_counts()
        .rename_axis("date")
        .reset_index(name="count")
    ).sort_values(by=["date"])
    return grouped_by_hour.set_index("date")


def plot_hourly_coverage(df, title):
    df_by_hour = group_df_by_hour(df)
    rolling_average = df_by_hour.rolling("12h").mean()

    fig, ax = plt.subplots()

    ax.plot(
        df_by_hour["count"], label="Hourly", marker=".", linestyle="-", linewidth=0.5
    )
    ax.plot(
        rolling_average["count"],
        marker=".",
        linestyle="-",
        label="12-Hour Rolling Mean",
    )

    ax.legend()

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    # mdates.HourLocator(interval = 12)
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))

    ax.set_title("Coverage for '{}' (total={:,})".format(title, len(df.index)))

    return fig
