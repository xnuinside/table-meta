from typing import List, Dict, Union
from table_meta import TableMeta, Type


def get_primary_keys(columns: List[Dict]) -> List[str]:
    primary_keys = []
    for column in columns:
        if column.get("properties", {}).get("primary_key"):
            primary_keys.append(column["name"])
    return primary_keys


def prepare_columns_data(columns: List[Dict]) -> List[Dict]:
    for column in columns:
        if column["type"] is None:
            if column["default"]:
                column["type"] = type(column["default"]).__name__
    return columns


def convert_table(model) -> TableMeta:
    model["table_name"] = model["name"]
    model["columns"] = prepare_columns_data(model["attrs"])
    model["properties"]["indexes"] = model["properties"].get("indexes") or []
    model["primary_key"] = get_primary_keys(model["columns"])
    return TableMeta(**model)


def convert_types(model: Dict) -> Type:
    model["type_name"] = model["name"]
    model["base_type"] = model["parents"][-1]
    return Type(**model)


def models_to_meta(data: List[Dict]) -> Dict[str, Union[TableMeta, Type]]:

    output = {"tables": [], "types": []}

    for model in data:
        if "Enum" in model["parents"]:
            output["types"].append(convert_types(model))
        else:
            output["tables"].append(convert_table(model))

    return output
