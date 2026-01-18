# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.2] - 2026-01-18

### Added

- New example YAML datasets materials/data_examples/ (menus, layouts, scrolls, selects, calendars, counters, multiwidgets, callbacks).
- Comprehensive test suite with unit, integration, and functional tests covering core components, achieving 91% code coverage.

### Changed

- Project restructured: renamed from dialog-yaml to dialog-yml, source code moved to src/dialog_yml/, all imports updated, package name changed in configuration files, middleware parameter renamed, and internal imports adjusted to reflect new package structure.
- Examples relocated to external repository (dialog-yml-examples).
- Test data file extensions standardized from .yaml to .yml.
- Documentation updated to reflect project renaming with README badges showing 91% coverage.
- Build system: Makefile updated with separate test targets, fail-fast options, PYTEST_ADDOPTS support, and coverage restricted to src directory; pyproject.toml classifiers updated to include OS Independent.
- Core functionality: DialogYAMLBuilder now stores empty dir path by default and uses internal fields in _build(); YAML reader supports both .yaml and .yml resolution with fallback; input widget defaults content_types to ANY when unspecified; NotifyModel migrated to pydantic v2 StringConstraints.
- Path handling improved: replaced all os.path.join calls with pathlib.Path for better readability and robustness.
- Dependencies: Updated aiogram-dialog version constraint from ~=2.4.0 to ~=2.4 to align with tested matrix.
- Development environment: VSCode settings configured for unittest integration; MessageInputModel.validate_content_types now raises validation errors instead of silently defaulting to ANY, improving error detection.

### Removed

- Legacy flat test files replaced by reorganized test suites.
- Development environment file (.env.dev) removed.

### Internal

- Test adjustments implemented for functions and widgets to match new behaviors and structure.

## [0.1.1] - 2026-01-18

### Added

- States property with dot-notation access to FSM states.

### Changed

- Enhanced package configuration and build process.
- Added dev environment config and updated dependency specifiers.
- Reorganized project structure and move core module to src.

### Documentation

- Added Russian translation and improved README documentation.
- Expanded documentation with architecture diagrams and function usage examples.

### Fixed

- Corrected state registration logic in `YAMLStatesManager`, particularly for custom `StatesGroup` classes.
- Improved state mapping and discovery within state groups.

## [0.1.0] - 2023-10-12

### Added

- Major refactor of `DialogYAMLBuilder` and related classes.
- Custom states and models registration.
- Separated factory logic into an independent class `YAMLModelFactory`.
- Created an abstract class `YAMLModel` for implementing models.
- "FuncRegistry" as a singleton class.
- Redesigned the logic of 'YAMLDialogStatesHolder', renamed to `YAMLStatesBuilder`.
- Redesigned the logic of registration in `FuncRegistry` and creation of `FuncModel`.
- Implemented other widgets and tests.
- Implemented kbd widgets, windows and dialogs.

### Fixed

- Refactored callback handling and updated examples.
- Corrected creation of a formatted states names for `YAMLStatesBuilder`.
- Fixed loading mega example.
- Re-thought the logic of the `YAMLModel` model factory class.
