# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.2] - 2026-01-18

### Changed

- Project renamed from dialog-yaml to dialog-yml
- Source code moved from src/ to src/dialog_yml/
- All imports changed from dialog_yaml to dialog_yml
- Examples moved to external repository (dialog-yml-examples)
- Test data extensions changed from .yaml to .yml
- Updated documentation to reflect new naming
- Updated Makefile to work with new examples location
- Package name changed in pyproject.toml and setup.cfg
- Middleware parameter renamed from dialog_yaml to dialog_yml
- Various internal imports updated to reflect new package structure
- Removed .env.dev file

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
