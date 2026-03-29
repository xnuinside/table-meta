# Changelog
All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog 1.0.0, and this project adheres to Semantic Versioning.

## [Unreleased]
### Added
- None.

### Changed
- None.

### Fixed
- None.

## [1.0.0] - 2026-03-29
### Added
- Added `tox` with test environments for Python 3.9, 3.10, 3.11, 3.12, 3.13, plus a lint environment.
- Added branch coverage reporting with a `100%` coverage gate.
- Added comprehensive tests for model validation and conversion paths.

### Changed
- Migrated the library to Pydantic v2 APIs and updated validation/configuration code to current patterns.
- Raised the minimum supported Python version to 3.9.
- Switched the canonical changelog to `CHANGELOG.md`.
- Bumped the package version to `1.0.0` for the breaking runtime/dependency changes.

### Fixed
- `ManyToMany` columns that reference a model field like `Model.field` now resolve the field type correctly during `models_to_meta()` conversion.
- Table/model conversion helpers no longer mutate the caller's input data in place.

## [0.3.2] - 2022-01-15
### Added
- Added `comment` attribute to `Column`.

## [0.3.0] - 2022-01-15
### Added
- Added type lookup for columns with foreign keys from model input.

### Fixed
- Fixed populating `Column` details such as `unique` and `primary_key` from `py-models-parser` input.

## [0.2.2] - 2022-01-07
### Added
- Added `if_not_exists` to table properties.

## [0.2.1] - 2022-01-05
### Added
- Added support for parsing `dataset` as `table_schema` and `project` fields to support BigQuery metadata.
- Added HQL table properties support.

### Changed
- Updated dependencies.

## [0.1.5] - 2021-08-22
### Added
- Added `attrs` field to `Type` to store values from `py-models-parser` output.

## [0.1.3] - 2021-08-15
### Added
- Added `parents` to `Type` and `Table`.

## [0.1.1] - 2021-08-15
### Fixed
- Fixed dependencies for Python 3.6.

## [0.1.0] - 2021-08-15
### Added
- Moved Table Meta from O!MyModels into a separate reusable library for use in fakeme.
