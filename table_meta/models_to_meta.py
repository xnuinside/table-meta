from __future__ import annotations

from copy import deepcopy
from typing import Any

from .model import TableMeta, Type


def get_primary_keys(columns: list[dict[str, Any]]) -> list[str]:
    return [
        column["name"]
        for column in columns
        if column.get("properties", {}).get("primary_key")
    ]


def populate_data_from_properties(column: dict[str, Any]) -> dict[str, Any]:
    if column.get("properties", {}):
        column.update(column["properties"])
    return column


def prepare_columns_data(
    columns: list[dict[str, Any]], full_data: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    prepared_columns = []

    for raw_column in columns:
        column = populate_data_from_properties(deepcopy(raw_column))

        if column.get("type") is None and column.get("default") is not None:
            column["type"] = type(column["default"]).__name__

        if column.get("type") == "ManyToMany":
            foreign_key = column.get("properties", {}).get("foreign_key")
            if not foreign_key or "." not in foreign_key:
                column["type"] = "int"
            else:
                model_name, field_name = foreign_key.rsplit(".", 1)
                for model in full_data:
                    if model_name == model["name"]:
                        for attr in model.get("attrs", []):
                            if attr["name"] == field_name:
                                column["type"] = attr["type"]
                                break
                        break

        prepared_columns.append(column)

    return prepared_columns


def convert_table(model: dict[str, Any], full_data: list[dict[str, Any]]) -> TableMeta:
    model_data = deepcopy(model)
    model_data["table_name"] = model_data["name"]
    model_data["columns"] = prepare_columns_data(model_data["attrs"], full_data)
    model_data["properties"] = deepcopy(model_data.get("properties") or {})
    model_data["properties"]["indexes"] = model_data["properties"].get("indexes") or []
    model_data["primary_key"] = get_primary_keys(model_data["columns"])
    return TableMeta.model_validate(model_data)


def convert_types(model: dict[str, Any]) -> Type:
    model_data = deepcopy(model)
    model_data["type_name"] = model_data["name"]
    model_data["base_type"] = model_data["parents"][-1]
    return Type.model_validate(model_data)


def models_to_meta(data: list[dict[str, Any]]) -> dict[str, list[TableMeta | Type]]:
    output = {"tables": [], "types": []}

    for model in data:
        if "Enum" in model["parents"]:
            output["types"].append(convert_types(model))
        else:
            output["tables"].append(convert_table(model, data))

    return output
