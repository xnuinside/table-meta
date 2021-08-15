from typing import Dict, Union
from table_meta import TableMeta, Type


def ddl_to_meta(data: Dict) -> Dict[str, Union[TableMeta, Type]]:
    """
        this method expected output from simple ddl parser that sorted by types
        that mean you need to use group_by_type=True flag in simple-ddl-parser .run() method
    """
    output = {"tables": [], "types": []}

    for table in data["tables"]:
        output["tables"].append(TableMeta(**table))

    for _type in data["types"]:
        output["types"].append(Type(**_type))

    return output
