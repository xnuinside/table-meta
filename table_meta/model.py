from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class ColumnBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    type: str
    size: Optional[Union[str, int, Tuple[Any, ...]]] = None


class HQLProperties(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    clustered_by: Optional[List[Any]] = None
    location: Optional[str] = None
    external: Optional[bool] = None
    row_format: Optional[str] = None
    fields_terminated_by: Optional[str] = None
    lines_terminated_by: Optional[str] = None
    map_keys_terminated_by: Optional[str] = None
    collection_items_terminated_by: Optional[str] = None
    stored_as: Optional[str] = None


class TableProperties(HQLProperties):
    indexes: Optional[List[Any]] = None
    alter: Optional[List[Any]] = None
    tablespace: Optional[str] = None
    partitioned_by: Optional[List[ColumnBase]] = None
    if_not_exists: Optional[bool] = None


class Column(ColumnBase):
    primary_key: bool = False
    unique: bool = False
    default: Any = None
    nullable: bool = True
    identifier: Optional[bool] = None
    generated_as: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None
    references: Optional[Dict[str, Any]] = None
    foreign_key: Optional[str] = None
    comment: Optional[str] = None

    @field_validator("size", mode="before")
    @classmethod
    def size_must_contain_space(cls, value: Any) -> Any:
        if isinstance(value, str) and value.isnumeric():
            return int(value)
        return value


class TableMeta(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: str = Field(alias="table_name")
    field_schema: Optional[str] = Field(default=None, alias="schema")
    dataset: Optional[str] = None
    columns: List[Column]
    indexes: Optional[List[Dict[str, Any]]] = Field(default=None, alias="index")
    alter: Dict[str, Any] = Field(default_factory=dict)
    checks: Optional[List[Dict[str, Any]]] = None
    properties: TableProperties = Field(default_factory=TableProperties)
    primary_key: List[Any]
    parents: Optional[List[str]] = None
    project: Optional[str] = None

    @property
    def table_schema(self) -> Optional[str]:
        return self.field_schema or self.dataset

    @model_validator(mode="before")
    @classmethod
    def set_properties(cls, values: Any) -> Any:
        if not isinstance(values, dict):
            return values

        field_names = set(cls.model_fields)
        aliases = {field.alias for field in cls.model_fields.values() if field.alias}
        properties = {
            key: value
            for key, value in values.items()
            if key not in field_names and key not in aliases
        }

        values = dict(values)
        existing_properties = dict(values.get("properties") or {})
        existing_properties.update(properties)
        values["properties"] = existing_properties

        return values


class Type(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(alias="type_name")
    base_type: str
    parents: Optional[List[str]] = None
    properties: Optional[Dict[str, Any]] = None
    attrs: Optional[List[Dict[str, Any]]] = None
