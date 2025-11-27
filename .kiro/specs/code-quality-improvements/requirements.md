# Requirements Document

## Introduction

This document defines the requirements for improving the code quality of the iztro-py library. The library is a pure Python implementation of Zi Wei Dou Shu (紫微斗数) astrology calculations, already published on PyPI. The improvements focus on fixing type system issues, cleaning up the codebase, improving test coverage, and enhancing documentation.

## Glossary

- **iztro-py**: The Python library for Zi Wei Dou Shu astrology calculations
- **mypy**: A static type checker for Python
- **ruff**: A fast Python linter
- **Type Annotation**: Python syntax for declaring expected types of variables, parameters, and return values
- **Test Coverage**: The percentage of code executed during test runs
- **FunctionalPalace**: An enhanced Palace class with additional query methods
- **FunctionalStar**: An enhanced Star class with additional query methods
- **Pydantic**: A data validation library using Python type annotations

## Requirements

### Requirement 1

**User Story:** As a developer using iztro-py, I want the library to pass mypy type checking without errors, so that I can rely on type hints for IDE support and catch type-related bugs early.

#### Acceptance Criteria

1. WHEN mypy is run on the src directory THEN the system SHALL report zero type errors
2. WHEN FunctionalPalace is used in place of Palace THEN the type system SHALL recognize the inheritance relationship correctly
3. WHEN FunctionalStar is used in place of Star THEN the type system SHALL recognize the inheritance relationship correctly
4. WHEN methods return subclass instances THEN the return type annotations SHALL accurately reflect the actual return types

### Requirement 2

**User Story:** As a maintainer of iztro-py, I want the root directory to be clean and organized, so that the project structure is professional and easy to navigate.

#### Acceptance Criteria

1. WHEN a developer clones the repository THEN the root directory SHALL contain only essential project files (README, LICENSE, pyproject.toml, etc.)
2. WHEN debug or verification scripts exist THEN the system SHALL organize them in a dedicated scripts/ directory
3. WHEN the project is built THEN the build process SHALL exclude non-essential scripts from the distribution

### Requirement 3

**User Story:** As a developer using iztro-py, I want the code to pass ruff linting without warnings, so that the codebase follows consistent Python best practices.

#### Acceptance Criteria

1. WHEN ruff check is run on the project THEN the system SHALL report zero linting errors
2. WHEN f-strings are used THEN the system SHALL ensure all f-strings contain placeholders
3. WHEN imports are organized THEN the system SHALL place module-level imports at the top of files

### Requirement 4

**User Story:** As a maintainer of iztro-py, I want comprehensive test coverage for all modules, so that I can confidently make changes without introducing regressions.

#### Acceptance Criteria

1. WHEN tests are run with coverage THEN the overall coverage SHALL be at least 85%
2. WHEN the i18n module is tested THEN the coverage for i18n/__init__.py SHALL be at least 80%
3. WHEN the functional_star module is tested THEN the coverage for functional_star.py SHALL be at least 80%
4. WHEN the functional_surpalaces module is tested THEN the coverage for functional_surpalaces.py SHALL be at least 80%
5. WHEN the mutagen module is tested THEN the coverage for mutagen.py SHALL be at least 80%

### Requirement 5

**User Story:** As a developer using iztro-py, I want complete and accurate documentation, so that I can quickly understand how to use the library.

#### Acceptance Criteria

1. WHEN the README references documentation files THEN those files SHALL exist and contain relevant content
2. WHEN a Korean user reads the README THEN a README_KO.md file SHALL be available with Korean content
3. WHEN a developer wants to contribute THEN a CONTRIBUTING.md file SHALL provide contribution guidelines
