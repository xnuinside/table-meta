import table_meta


def test_models_in_place_in_init():
    assert "TableMeta" in dir(table_meta)
    assert "Type" in dir(table_meta)
    assert "ddl_to_meta" in dir(table_meta)
    assert "models_to_meta" in dir(table_meta)
