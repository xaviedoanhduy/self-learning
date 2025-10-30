import json
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol
import pandas as pd


@dataclass
class ReportConfig:
    input_file: str
    output_file: str
    start_date: datetime | None = None
    end_date: datetime | None = None


# ---- Reader ----
class SalesReader(Protocol):
    def read(self, input_file: str) -> pd.DataFrame: ...


class CSVSalesReader:
    def read(self, input_file: str) -> pd.DataFrame:
        return pd.read_csv(input_file, parse_dates=["date"])


# ---- Filters ----
class DateRangeFilter:
    def apply(self, df: pd.DataFrame, start_date: datetime | None, end_date: datetime | None) -> pd.DataFrame:
        if start_date:
            df = df[df["date"] >= pd.Timestamp(start_date)]
        if end_date:
            df = df[df["date"] <= pd.Timestamp(end_date)]
        return df


# ---- Metrics ----
class Metric(Protocol):
    def compute(self, df: pd.DataFrame) -> dict[str, object]: ...


class CustomerCountMetric:
    def compute(self, df: pd.DataFrame) -> dict[str, object]:
        return {"number_of_customers": int(df["name"].nunique())}


class AverageOrderValueMetric:
    def compute(self, df: pd.DataFrame) -> dict[str, object]:
        positive = df.loc[df["price"] > 0, "price"]
        avg = positive.mean() if not positive.empty else 0.0
        return {"average_order_value (pre-tax)": round(avg, 2)}


class ReturnPercentageMetric:
    def compute(self, df: pd.DataFrame) -> dict[str, object]:
        pct = (df["price"] < 0).mean() * 100 if not df.empty else 0.0
        return {"percentage_of_returns": round(pct, 2)}


class TotalSalesMetric:
    def compute(self, df: pd.DataFrame) -> dict[str, object]:
        total = df["price"].sum()
        return {"total_sales_in_period (pre-tax)": round(total, 2)}


# ---- Report Generator ----
class SalesReportGenerator:
    def __init__(self, reader: SalesReader, date_filter: DateRangeFilter, metrics: list[Metric]) -> None:
        self.reader = reader
        self.date_filter = date_filter
        self.metrics = metrics

    def generate_report(self, config: ReportConfig) -> dict[str, object]:
        df = self.reader.read(config.input_file)
        df = self.date_filter.apply(df, config.start_date, config.end_date)

        report_data = {
            "report_start": config.start_date.strftime("%Y-%m-%d") if config.start_date else "N/A",
            "report_end": config.end_date.strftime("%Y-%m-%d") if config.end_date else "N/A",
        }

        for metric in self.metrics:
            report_data.update(metric.compute(df))
        return report_data


# ---- Writer ----
class JSONReportWriter:
    def write(self, report_data: dict[str, object], output_file: str) -> None:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=4, ensure_ascii=False, default=str)


# ---- Main ----
def main() -> None:
    config = ReportConfig(
        input_file="sales_data.csv",
        output_file="sales_report.json",
        start_date=datetime(2023, 1, 1),
        end_date=datetime(2023, 12, 31),
    )

    reader = CSVSalesReader()
    date_filter = DateRangeFilter()
    metrics = [
        CustomerCountMetric(),
        AverageOrderValueMetric(),
        ReturnPercentageMetric(),
        TotalSalesMetric(),
    ]

    generator = SalesReportGenerator(reader, date_filter, metrics)
    report = generator.generate_report(config)

    writer = JSONReportWriter()
    writer.write(report, config.output_file)

    print(f"✅ Report generated successfully: {config.output_file}")


if __name__ == "__main__":
    main()
