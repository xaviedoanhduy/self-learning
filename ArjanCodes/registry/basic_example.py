import json

from typing import Any, Callable, Dict
from functools import wraps

Data = Dict[str, Any]
ExportFn = Callable[[Data], str]

exporters: Dict[str, ExportFn] = {}


def register_exporter(format_name: str) -> Callable[[ExportFn], ExportFn]:
    def decorator(func: ExportFn) -> ExportFn:
        @wraps(func)
        def wrapper(data: Data) -> str:
            return func(data)

        exporters[format_name] = wrapper
        return wrapper

    return decorator


@register_exporter("json")
def export_to_json(data: Data) -> str:
    return json.dumps(data, indent=4)


@register_exporter("xml")
def export_to_xml(data: Data) -> str:
    xml_items = [f"<{key}>{value}</{key}>" for key, value in data.items()]
    return "<root>\n" + "\n".join(xml_items) + "\n</root>"


@register_exporter("csv")
def export_to_csv(data: Data) -> str:
    csv_items = [f"{key},{value}" for key, value in data.items()]
    return "\n".join(csv_items)


@register_exporter("pdf")
def export_to_pdf(data: Data) -> str:
    pdf_content = "PDF Document\n\n"
    for key, value in data.items():
        pdf_content += f"{key}: {value}\n"
    return pdf_content


@register_exporter("yaml")
def export_to_yaml(data: Data) -> str:    
    print("Exporting data to YAML format.")
    yaml_items = [f"{key}: {value}" for key, value in data.items()]
    return "\n".join(yaml_items)


def export_data(data: Data, format_name: str) -> str:
    if format_name not in exporters:
        raise ValueError(f"Exporter for format '{format_name}' is not registered.")
    export_fn = exporters[format_name]
    return export_fn(data)


def main() -> None:
    sample_data: Data = {
        "name": "John Doe",
        "age": 30,
        "city": "New York"
    }

    for format_name in exporters.keys():
        print(f"\n--- Exporting to {format_name.upper()} ---")
        exported_content = export_data(sample_data, format_name)
        print(exported_content)


if __name__ == "__main__":
    main()
