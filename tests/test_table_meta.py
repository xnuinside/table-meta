from __future__ import annotations

from copy import deepcopy

import table_meta
from table_meta.ddl_to_meta import ddl_to_meta
from table_meta.model import Column, TableMeta, Type
from table_meta.models_to_meta import (
    convert_table,
    convert_types,
    get_primary_keys,
    models_to_meta,
    populate_data_from_properties,
    prepare_columns_data,
)


def test_models_in_place_in_init():
    assert "TableMeta" in dir(table_meta)
    assert "Type" in dir(table_meta)
    assert "ddl_to_meta" in dir(table_meta)
    assert "models_to_meta" in dir(table_meta)


def test_column_size_validator_converts_numeric_strings_only():
    numeric_column = Column(name="id", type="int", size="10")
    tuple_column = Column(name="coords", type="tuple", size=("10", "20"))

    assert numeric_column.size == 10
    assert tuple_column.size == ("10", "20")


def test_table_meta_aliases_collect_extra_properties_and_table_schema_fallback():
    table = TableMeta(
        table_name="events",
        dataset="analytics",
        columns=[{"name": "event_id", "type": "int"}],
        primary_key=["event_id"],
        index=[{"name": "idx_events_event_id"}],
        tablespace="fast_disk",
        if_not_exists=True,
    )

    assert table.name == "events"
    assert table.table_schema == "analytics"
    assert table.indexes == [{"name": "idx_events_event_id"}]
    assert table.properties.tablespace == "fast_disk"
    assert table.properties.if_not_exists is True


def test_table_meta_default_factories_are_not_shared():
    first = TableMeta(
        table_name="users",
        schema="public",
        columns=[{"name": "id", "type": "int"}],
        primary_key=["id"],
    )
    second = TableMeta(
        table_name="roles",
        schema="public",
        columns=[{"name": "id", "type": "int"}],
        primary_key=["id"],
    )

    first.alter["drop"] = ["old_column"]
    first.properties.indexes = ["idx_users_id"]

    assert second.alter == {}
    assert second.properties.indexes is None
    assert first.table_schema == "public"


def test_table_meta_model_validate_accepts_existing_instance():
    table = TableMeta(
        table_name="audit_log",
        schema="public",
        columns=[{"name": "id", "type": "int"}],
        primary_key=["id"],
    )

    assert TableMeta.model_validate(table) is table


def test_table_meta_set_properties_passthrough_for_non_dict_values():
    assert TableMeta.set_properties("raw-value") == "raw-value"


def test_populate_data_from_properties_and_primary_key_extraction():
    column = {
        "name": "id",
        "type": "int",
        "properties": {"primary_key": True, "unique": True},
    }
    untouched = {"name": "title", "type": "str", "properties": {}}

    populated = populate_data_from_properties(column)
    untouched_populated = populate_data_from_properties(untouched)

    assert populated["primary_key"] is True
    assert populated["unique"] is True
    assert untouched_populated == untouched
    assert get_primary_keys([column, untouched]) == ["id"]


def test_prepare_columns_data_resolves_defaults_and_many_to_many_types():
    full_data = [
        {
            "name": "Order",
            "parents": ["Base"],
            "attrs": [{"name": "id", "type": "uuid", "properties": {}}],
            "properties": {},
        }
    ]
    columns = [
        {"name": "count", "type": None, "default": 0, "properties": {}},
        {
            "name": "order_id",
            "type": "ManyToMany",
            "properties": {"foreign_key": "Order.id"},
        },
        {
            "name": "fallback_fk",
            "type": "ManyToMany",
            "properties": {"foreign_key": "id"},
        },
    ]

    prepared = prepare_columns_data(columns, full_data)

    assert prepared[0]["type"] == "int"
    assert prepared[1]["type"] == "uuid"
    assert prepared[2]["type"] == "int"
    assert columns[0]["type"] is None


def test_prepare_columns_data_keeps_many_to_many_when_reference_cannot_be_resolved():
    full_data = [
        {
            "name": "Order",
            "parents": ["Base"],
            "attrs": [
                {"name": "id", "type": "uuid", "properties": {}},
                {"name": "external_id", "type": "str", "properties": {}},
            ],
            "properties": {},
        }
    ]
    columns = [
        {
            "name": "missing_model",
            "type": "ManyToMany",
            "properties": {"foreign_key": "Invoice.id"},
        },
        {
            "name": "missing_field",
            "type": "ManyToMany",
            "properties": {"foreign_key": "Order.number"},
        },
        {
            "name": "resolved_second_attr",
            "type": "ManyToMany",
            "properties": {"foreign_key": "Order.external_id"},
        },
    ]

    prepared = prepare_columns_data(columns, full_data)

    assert prepared[0]["type"] == "ManyToMany"
    assert prepared[1]["type"] == "ManyToMany"
    assert prepared[2]["type"] == "str"


def test_convert_table_and_convert_type_do_not_mutate_input():
    table_model = {
        "name": "User",
        "parents": ["Base"],
        "attrs": [
            {"name": "id", "type": "int", "properties": {"primary_key": True}},
            {
                "name": "role_id",
                "type": "ManyToMany",
                "properties": {"foreign_key": "Role.id"},
            },
        ],
        "properties": {},
    }
    role_model = {
        "name": "Role",
        "parents": ["Base"],
        "attrs": [{"name": "id", "type": "uuid", "properties": {}}],
        "properties": {},
    }
    enum_model = {
        "name": "Status",
        "parents": ["Enum", "str"],
        "attrs": [{"name": "NEW"}],
        "properties": {"scope": "shared"},
    }

    original_table_model = deepcopy(table_model)
    original_enum_model = deepcopy(enum_model)

    table = convert_table(table_model, [table_model, role_model, enum_model])
    enum_type = convert_types(enum_model)

    assert table.name == "User"
    assert table.columns[1].type == "uuid"
    assert table.primary_key == ["id"]
    assert table_model == original_table_model
    assert enum_type.name == "Status"
    assert enum_type.base_type == "str"
    assert enum_model == original_enum_model


def test_models_to_meta_and_ddl_to_meta_convert_expected_objects():
    model_data = [
        {
            "name": "User",
            "parents": ["Base"],
            "attrs": [
                {"name": "id", "type": "int", "properties": {"primary_key": True}}
            ],
            "properties": {"indexes": [{"name": "idx_user_id"}]},
        },
        {
            "name": "Color",
            "parents": ["Enum", "str"],
            "attrs": [{"name": "BLUE"}],
            "properties": {},
        },
    ]
    ddl_data = {
        "tables": [
            {
                "table_name": "accounts",
                "schema": "public",
                "columns": [{"name": "id", "type": "int", "size": "4"}],
                "primary_key": ["id"],
                "tablespace": "archive",
            }
        ],
        "types": [
            {
                "type_name": "account_status",
                "base_type": "text",
                "parents": ["Enum", "text"],
            }
        ],
    }

    models_result = models_to_meta(model_data)
    ddl_result = ddl_to_meta(ddl_data)

    assert len(models_result["tables"]) == 1
    assert len(models_result["types"]) == 1
    assert models_result["tables"][0].properties.indexes == [{"name": "idx_user_id"}]
    assert isinstance(ddl_result["tables"][0], TableMeta)
    assert isinstance(ddl_result["types"][0], Type)
    assert ddl_result["tables"][0].columns[0].size == 4
    assert ddl_result["tables"][0].properties.tablespace == "archive"


def test_empty_inputs_are_supported():
    assert ddl_to_meta({}) == {"tables": [], "types": []}
    assert models_to_meta([]) == {"tables": [], "types": []}
