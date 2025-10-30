import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable

import pandas as pd


type MetricFunc = Callable[[pd.DataFrame], dict[str, Any]]


@dataclass
class ReportConfig:
    input_file: str
    output_file: str
    start_date: datetime | None = None
    end_date: datetime | None = None
    metrics: list[MetricFunc] = field(default_factory=list)


def read_sales_data(input_file: str) -> pd.DataFrame:
    return pd.read_csv(input_file, parse_dates=["date"])


def filter_by_date_range(
    df: pd.DataFrame,
    start_date: datetime | None,
    end_date: datetime | None,
) -> pd.DataFrame:
    if start_date:
        df = df[df["date"] >= pd.Timestamp(start_date)]
    if end_date:
        df = df[df["date"] <= pd.Timestamp(end_date)]
    return df


def compute_customer_count(df: pd.DataFrame) -> dict[str, Any]:
    return {"number_of_customers": int(df["name"].nunique())}

def compute_average_order_value(df: pd.DataFrame) -> dict[str, Any]:
    positive = df.loc[df["price"] > 0, "price"]
    avg = positive.mean() if not positive.empty else 0.0
    return {"average_order_value (pre-tax)": round(avg, 2)}


def compute_return_percentage(df: pd.DataFrame) -> dict[str, Any]:
    pct = (df["price"] < 0).mean() * 100 if not df.empty else 0.0
    return {"percentage_of_returns": round(pct, 2)}


def compute_total_sales(df: pd.DataFrame) -> dict[str, Any]:
    total = df["price"].sum()
    return {"total_sales_in_period (pre-tax)": round(total, 2)}


def generate_report_data(config: ReportConfig) -> dict[str, Any]:
    df = read_sales_data(config.input_file)
    df = filter_by_date_range(df, config.start_date, config.end_date)

    report_data: dict[str, Any] = {}
    for metric in config.metrics:
        report_data.update(metric(df))

    report_data["report_start"] = (
        config.start_date.strftime("%Y-%m-%d") if config.start_date else "N/A"
    )
    report_data["report_end"] = (
        config.end_date.strftime("%Y-%m-%d") if config.end_date else "N/A"
    )

    return report_data

def write_report_to_json(report_data: dict[str, Any], output_file: str) -> None:
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=4, ensure_ascii=False, default=str)
    print(f"✅ Report generated successfully: {output_file}")


def main() -> None:
    config = ReportConfig(
        input_file="sales_data.csv",
        output_file="sales_report.json",
        start_date=datetime(2023, 1, 1),
        end_date=datetime(2023, 12, 31),
        metrics=[
            compute_customer_count,
            compute_average_order_value,
            compute_return_percentage,
            compute_total_sales,
        ],
    )

    report_data = generate_report_data(config)
    write_report_to_json(report_data, config.output_file)


if __name__ == "__main__":
    main()
