import json
import pandas as pd
from datetime import datetime
from pathlib import Path


class MessySaleReport:
    def generate_report(
        self, 
        input_file: str,
        output_file: str,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> None:
        # Check if input file exists
        if not Path(input_file).exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")

        # Read CSV and parse the 'date' column as datetime
        try:
            df = pd.read_csv(input_file, parse_dates=["date"])
        except Exception as e:
            raise ValueError(f"Failed to read CSV file: {e}")

        # Ensure required columns exist
        required_cols = {"name", "price", "date"}
        if not required_cols.issubset(df.columns):
            raise KeyError(f"Missing columns: {required_cols - set(df.columns)}")

        # Convert start and end dates to pandas timestamps once
        start_ts = pd.Timestamp(start_date) if start_date else None
        end_ts = pd.Timestamp(end_date) if end_date else None

        # Filter data based on date range
        if start_ts is not None:
            df = df[df["date"] >= start_ts]
        if end_ts is not None:
            df = df[df["date"] <= end_ts]

        if df.empty:
            print("⚠️ No data found in the specified date range.")
            return

        # Calculate unique customers
        num_customers = df["name"].nunique()  # could be 'customer_id' if available

        # Filter out positive and negative prices
        positive_prices = df.loc[df["price"] > 0, "price"]
        avg_order = positive_prices.mean() if not positive_prices.empty else 0

        # Calculate percentage of returns
        # using boolean mean() for cleaner logic
        return_ptc = (df["price"] < 0).mean() * 100 if not df.empty else 0

        # Calculate total sales (including negative returns)
        total_sales = df["price"].sum()

        # Prepare report dictionary
        report_vals = {
            "report_start": start_ts.strftime("%Y-%m-%d") if start_ts else "N/A",
            "report_end": end_ts.strftime("%Y-%m-%d") if end_ts else "N/A",
            "number_of_customers": int(num_customers),
            "average_order_value (pre-tax)": round(avg_order, 2),
            "percentage_of_returns": round(return_ptc, 2),
            "total_sales_in_period (pre-tax)": round(total_sales, 2),
        }

        # Ensure output directory exists before writing
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)

        # Write JSON report
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report_vals, f, indent=4, ensure_ascii=False)

        print(f"✅ Report generated successfully: {output_file}")


def main() -> None:
    report = MessySaleReport()
    report.generate_report(
        input_file="sales_data.csv",
        output_file="reports/sales_report.json",
        start_date=datetime(2023, 1, 1),
        end_date=datetime(2023, 12, 31),
    )


if __name__ == "__main__":
    main()
