from typing import List, Dict, Union
from table_meta import TableMeta, Type


def get_primary_keys(columns: List[Dict]) -> List[str]:
    primary_keys = []
    for column in columns:
        if column.get("properties", {}).get("primary_key"):
            primary_keys.append(column["name"])
    return primary_keys


def populate_data_from_properties(column: Dict):
    if column.get("properties", {}):
        column.update({
            _property: value for _property, value in column["properties"].items()
            if _property not in ['foreign_key']})


def prepare_columns_data(columns: List[Dict], full_data: Dict) -> List[Dict]:
    # todo: refactor it
    for column in columns:
        populate_data_from_properties(column)
        if column["type"] is None:
            if column["default"]:
                column["type"] = type(column["default"]).__name__
        if column["type"] == "ManyToMany":
            column["foreign_key"] = True
            foreign_key = column["properties"]['foreign_key']
            if '.' not in foreign_key:
                field_name = "id"
                column["type"] = 'int'
            else:
                field_name = foreign_key.split('.')[-1]
            for model in full_data:
                if field_name == model["name"]:
                    for attr in model["attrs"]:
                        if attr['name'] == field_name:
                            column["type"] = attr['type']
                            break
    return columns


def convert_table(model: Dict, full_data: Dict) -> TableMeta:
    print(1)
    print(full_data)
    model["table_name"] = model["name"]
    model["columns"] = prepare_columns_data(model["attrs"], full_data)
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
            output["tables"].append(convert_table(model, data))

    return output
