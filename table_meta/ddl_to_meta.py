from __future__ import annotations

from typing import Any

from .model import TableMeta, Type


def ddl_to_meta(data: dict[str, Any]) -> dict[str, list[TableMeta | Type]]:
    """
    this method expected output from simple ddl parser that sorted by types
    that mean you need to use group_by_type=True flag in simple-ddl-parser .run() method
    """
    output = {"tables": [], "types": []}

    for table in data.get("tables", []):
        output["tables"].append(TableMeta.model_validate(table))

    for _type in data.get("types", []):
        output["types"].append(Type.model_validate(_type))

    return output
