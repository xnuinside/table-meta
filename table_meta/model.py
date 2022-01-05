from pydantic import BaseModel, Field, validator, root_validator
from typing import List, Optional, Union, Dict, Tuple


class ColumnBase(BaseModel):
    name: str
    type: str
    size: Optional[Union[str, int, Tuple]]

class HQLProperties(BaseModel):
    clustered_by: Optional[List]
    location: Optional[str]
    external: Optional[bool]
    row_format: Optional[str]
    fields_terminated_by: Optional[str]
    lines_terminated_by: Optional[str]
    map_keys_terminated_by: Optional[str]
    collection_items_terminated_by: Optional[str]
    stored_as: Optional[str]
    
class TableProperties(HQLProperties):

    indexes: Optional[List]
    alter: Optional[List]
    tablespace: Optional[str]
    partitioned_by: Optional[List[ColumnBase]]
    if_not_exists: Optional[bool]
    
class Column(ColumnBase):

    primary_key: bool = False
    unique: bool = False
    default: Optional[str]
    nullable: bool = True
    identifier: Optional[bool]
    generated_as: Optional[str]
    other_properties: Optional[Dict]
    references: Optional[Dict]

    @validator("size")
    def size_must_contain_space(cls, v):
        if isinstance(v, str) and v.isnumeric():
            return int(v)
        return v


class TableMeta(BaseModel):
    name: str = Field(alias="table_name")
    field_schema: Optional[str] = Field(alias="schema")
    dataset: Optional[str]
    columns: List[Column]
    indexes: Optional[List[Dict]] = Field(alias="index")
    alter: Optional[Dict] = {}
    checks: Optional[List[Dict]]
    properties: Optional[TableProperties]
    primary_key: List
    parents: Optional[List[str]]
    project: Optional[str]

    @property
    def table_schema(self):
        return self.field_schema or self.dataset
    
    # add root validator to parse incoming fields & wrote them as properties
    @root_validator(pre=True)
    def set_properties(cls, values: Dict):
        properties = {}
        print("SET properties ", values)
        print(values.keys())
        for key, value in values.items():
            if key not in cls.__fields__:
                properties[key] = value
        if not values.get("properties"):
            values["properties"] = {}
        values["properties"].update(properties)

        return values
    
    class Config:
        """ pydantic class config """

        arbitrary_types_allowed = True


class Type(BaseModel):
    name: str = Field(alias="type_name")
    base_type: str
    parents: Optional[List[str]]
    properties: Optional[Dict]
    attrs: Optional[List[Dict]]
