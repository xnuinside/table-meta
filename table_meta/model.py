from pydantic import BaseModel, Field, validator
from typing import List, Optional, Union, Dict, Tuple


class TableProperties(BaseModel):

    indexes: List


class Column(BaseModel):

    name: str
    type: str
    size: Optional[Union[str, int, Tuple]]
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
    table_schema: Optional[str] = Field(alias="schema")
    columns: List[Column]
    indexes: Optional[List[Dict]] = Field(alias="index")
    alter: Optional[Dict] = {}
    checks: Optional[List[Dict]]
    properties: Optional[TableProperties]
    primary_key: List
    parents: Optional[List[str]]

    class Config:
        """ pydantic class config """

        arbitrary_types_allowed = True


class Type(BaseModel):
    name: str = Field(alias="type_name")
    base_type: str
    parents: Optional[List[str]]
    properties: Optional[Dict]
    attrs: Optional[List[Dict]]

