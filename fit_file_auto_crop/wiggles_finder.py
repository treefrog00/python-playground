import polars as pl
from suspicious_activities import suspicious_speeds
from lat_lon_code import lat_lon_distance

# Define small constant to prevent division by zero when timestamps are identical
EPSILON = 0.000001  # 1 microsecond


def categorise_speed(speed, suspicious_speed):
    if speed <= 1:
        return "slow"
    elif speed >= suspicious_speed:
        return "suspicious"
    else:
        return "medium"


def munge_wiggles_data(fit_data):
    sport = fit_data.session_metadata["sport"]
    suspicious_speed = suspicious_speeds[sport]

    data = [
        {
            "distance": record.get_value("distance"),
            "timestamp": record.get_value("timestamp"),
            "lat": (
                record.get_value("position_lat") / ((2**32) / 360)
                if record.has_field("position_lat")
                else None
            ),
            "lon": (
                record.get_value("position_long") / ((2**32) / 360)
                if record.has_field("position_long")
                else None
            ),
        }
        for record in fit_data.records
    ]

    # Convert to Polars DataFrame and add index
    df = pl.DataFrame(data)
    df = df.with_row_index("index")

    # Calculate velocities (change in position over time)
    df = df.with_columns(
        [
            pl.col("lat").diff().alias("lat_velocity"),
            pl.col("lon").diff().alias("lon_velocity"),
        ]
    )

    # Detect direction changes (when velocity changes sign)
    df = df.with_columns(
        [
            (
                pl.col("lat_velocity").shift().is_not_null()
                & (pl.col("lat_velocity") * pl.col("lat_velocity").shift() < 0)
            )
            .fill_null(False)
            .alias("lat_dir_change"),
            (
                pl.col("lon_velocity").shift().is_not_null()
                & (pl.col("lon_velocity") * pl.col("lon_velocity").shift() < 0)
            )
            .fill_null(False)
            .alias("lon_dir_change"),
        ]
    )

    # Add lat/lon of previous row
    df = df.with_columns(
        [
            pl.col("lat").shift().alias("prev_lat"),
            pl.col("lon").shift().alias("prev_lon"),
        ]
    )

    # Create a group identifier that changes when direction changes
    df = df.with_columns(
        [
            (pl.col("lat_dir_change") & pl.col("lon_dir_change"))
            .cast(pl.Int32)
            .cum_sum()
            .alias("direction_group")
        ]
    )

    debug = False

    if debug:
        cfg = pl.Config()
        cfg.set_tbl_cols(100)
        cfg.set_tbl_rows(100)
        print(
            df.select(
                pl.col("direction_group"),
                pl.col("lat"),
                pl.col("lon"),
                pl.col("lat_velocity"),
                pl.col("lon_velocity"),
            ).head(100)
        )

    # Starting location is first non-null lat/lon
    first_valid_row = df.filter(
        pl.col("lat").is_not_null() & pl.col("lon").is_not_null()
    ).head(1)
    route_start_lat = first_valid_row["lat"][0]
    route_start_lon = first_valid_row["lon"][0]

    # Create merged dataframe that combines rows with same direction
    merged_df = (
        df.group_by("direction_group")
        .agg(
            [
                pl.col("index").first().alias("start_index"),
                pl.col("index").last().alias("end_index"),
                pl.col("lat").drop_nulls().last().alias("lat"),
                pl.col("lon").drop_nulls().last().alias("lon"),
                pl.col("lat_velocity").last().alias("lat_velocity"),
                pl.col("lon_velocity").last().alias("lon_velocity"),
                pl.col("timestamp").first().alias("first_record_time"),
                pl.col("timestamp").last().alias("timestamp"),
                pl.col("distance").last().alias("distance"),
            ]
        )
        .sort("start_index")
    )

    # Add start_distance, start_time and start lat/lon as the end values of the previous row (or initial values for first row)
    # Note this is different to the first entry of each group - the theory is that each segment starts at the end of the previous one, and that each lat/lon/time etc is treated as recording the end of a line segment
    merged_df = merged_df.with_columns(
        [
            pl.col("distance").shift().fill_null(0.0).alias("start_distance"),
            pl.col("timestamp")
            .shift()
            .fill_null(pl.col("first_record_time"))
            .alias("start_time"),
            pl.col("lat").shift().fill_null(route_start_lat).alias("start_lat"),
            pl.col("lon").shift().fill_null(route_start_lon).alias("start_lon"),
        ]
    )

    # Add distance to start calculation for each segment's start point
    merged_df = merged_df.with_columns(
        [
            pl.struct(["lat", "lon"])
            .map_elements(
                lambda x: (
                    lat_lon_distance(
                        route_start_lat, route_start_lon, x["lat"], x["lon"]
                    )
                    * 1000
                    if x["lat"] is not None and x["lon"] is not None
                    else None
                )
            )
            .alias("distance_to_start_m")
        ]
    )

    # Calculate segment distances and time differences
    merged_df = merged_df.with_columns(
        [
            (pl.col("distance") - pl.col("start_distance")).alias("segment_distance_m"),
            (
                (
                    pl.col("timestamp").cast(pl.Int64)
                    - pl.col("start_time").cast(pl.Int64)
                )
                / 1_000_000
            ).alias("time_diff_seconds"),
        ]
    )

    # Calculate speed in km/h, handling edge cases
    merged_df = merged_df.with_columns(
        [
            pl.when(pl.col("time_diff_seconds") > EPSILON)
            .then(
                (pl.col("segment_distance_m") / 1000.0)
                / (pl.col("time_diff_seconds") / 3600)
            )
            .otherwise(0.0)
            .alias("speed_kmh")
        ]
    )

    # Add speed category based on speed_kmh
    merged_df = merged_df.with_columns(
        [
            pl.col("speed_kmh")
            .map_elements(
                lambda x: categorise_speed(x, suspicious_speed), return_dtype=pl.Utf8
            )
            .alias("speed_category")
        ]
    )

    debug = True
    if debug:
        cfg = pl.Config()
        cfg.set_tbl_cols(100)
        cfg.set_tbl_rows(100)
        print(merged_df.head(100))

    return merged_df
