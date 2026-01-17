# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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