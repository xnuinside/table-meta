from __future__ import annotations

from typing import Any, Dict, List, Tuple, Union

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class ColumnBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    type: str
    size: Union[str, int, Tuple[Any, ...]] | None = None


class HQLProperties(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    clustered_by: List[Any] | None = None
    location: str | None = None
    external: bool | None = None
    row_format: str | None = None
    fields_terminated_by: str | None = None
    lines_terminated_by: str | None = None
    map_keys_terminated_by: str | None = None
    collection_items_terminated_by: str | None = None
    stored_as: str | None = None


class TableProperties(HQLProperties):
    indexes: List[Any] | None = None
    alter: List[Any] | None = None
    tablespace: str | None = None
    partitioned_by: List[ColumnBase] | None = None
    if_not_exists: bool | None = None


class Column(ColumnBase):
    primary_key: bool = False
    unique: bool = False
    default: Any = None
    nullable: bool = True
    identifier: bool | None = None
    generated_as: str | None = None
    properties: Dict[str, Any] | None = None
    references: Dict[str, Any] | None = None
    foreign_key: str | None = None
    comment: str | None = None

    @field_validator("size", mode="before")
    @classmethod
    def size_must_contain_space(cls, value: Any) -> Any:
        if isinstance(value, str) and value.isnumeric():
            return int(value)
        return value


class TableMeta(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: str = Field(alias="table_name")
    field_schema: str | None = Field(default=None, alias="schema")
    dataset: str | None = None
    columns: List[Column]
    indexes: List[Dict[str, Any]] | None = Field(default=None, alias="index")
    alter: Dict[str, Any] = Field(default_factory=dict)
    checks: List[Dict[str, Any]] | None = None
    properties: TableProperties = Field(default_factory=TableProperties)
    primary_key: List[Any]
    parents: List[str] | None = None
    project: str | None = None

    @property
    def table_schema(self) -> str | None:
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
    parents: List[str] | None = None
    properties: Dict[str, Any] | None = None
    attrs: List[Dict[str, Any]] | None = None
