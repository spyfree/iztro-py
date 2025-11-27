# Implementation Plan

- [x] 1. Fix type system issues in data/types.py
  - [x] 1.1 Change `List[Star]` to `Sequence[Star]` in Palace model for major_stars, minor_stars, adjective_stars
  - [x] 1.2 Change `List[Palace]` to `Sequence[Palace]` in Astrolabe model
  - [x] 1.3 Update imports to include Sequence from typing
  - _Requirements: 1.1, 1.2, 1.3, 1.4_

- [x] 2. Fix type annotations in functional_palace.py
  - [x] 2.1 Update __init__ to properly handle star list types
  - [x] 2.2 Fix get_star return type annotation
  - [x] 2.3 Ensure all method return types match actual returns
  - _Requirements: 1.2, 1.4_

- [x] 3. Fix type annotations in functional_star.py
  - [x] 3.1 Fix any type annotation issues in method signatures
  - [x] 3.2 Ensure palace() return type is correct
  - _Requirements: 1.3, 1.4_

- [x] 4. Fix type annotations in functional_surpalaces.py
  - [x] 4.1 Update constructor parameter types to use FunctionalPalace
  - [x] 4.2 Fix all_palaces() return type annotation
  - [x] 4.3 Ensure have/not_have methods work with correct types
  - _Requirements: 1.2, 1.4_

- [x] 5. Fix type annotations in functional_astrolabe.py
  - [x] 5.1 Fix palace() method return type
  - [x] 5.2 Fix star() method return type
  - [x] 5.3 Fix surrounded_palaces() method return type
  - [x] 5.4 Fix empty_palaces() and not_empty_palaces() return types
  - [x] 5.5 Fix to_iztro_dict() star_dict function parameter type
  - _Requirements: 1.1, 1.4_

- [x] 6. Fix type annotations in astro.py
  - [x] 6.1 Fix palaces parameter type when creating Astrolabe
  - _Requirements: 1.1, 1.4_

- [x] 7. Fix type annotations in star modules
  - [x] 7.1 Fix minor_star.py return type annotations
  - [x] 7.2 Fix major_star.py Star name argument type
  - _Requirements: 1.1, 1.4_

- [x] 8. Checkpoint - Verify mypy passes
  - Ensure all tests pass, ask the user if questions arise.

- [x] 9. Clean up root directory
  - [x] 9.1 Create scripts/ directory
  - [x] 9.2 Move debug scripts (check_*.py, debug_*.py) to scripts/
  - [x] 9.3 Move verification scripts (verify_*.py, *_verify.py, *_comparison.py) to scripts/
  - [x] 9.4 Update .gitignore if needed
  - [x] 9.5 Update MANIFEST.in to exclude scripts/ from distribution
  - _Requirements: 2.1, 2.2, 2.3_

- [x] 10. Fix ruff linting issues
  - [x] 10.1 Fix f-string without placeholders warnings in scripts
  - [x] 10.2 Fix module-level import issues in scripts
  - [x] 10.3 Run ruff --fix to auto-fix remaining issues
  - _Requirements: 3.1, 3.2, 3.3_

- [x] 11. Checkpoint - Verify ruff passes
  - Ensure all tests pass, ask the user if questions arise.

- [x] 12. Improve test coverage for i18n module
  - [x] 12.1 Add tests for set_language with unsupported language
  - [x] 12.2 Add tests for translate_dict function
  - [x] 12.3 Add tests for all supported languages loading
  - _Requirements: 4.1, 4.2_

- [x] 13. Improve test coverage for functional_star module
  - [x] 13.1 Add tests for with_brightness method
  - [x] 13.2 Add tests for with_mutagen method
  - [x] 13.3 Add tests for opposite_palace method
  - [x] 13.4 Add tests for surrounded_palaces method
  - [x] 13.5 Add tests for is_major, is_minor, is_bright, is_weak methods
  - _Requirements: 4.1, 4.3_

- [x] 14. Improve test coverage for functional_surpalaces module
  - [x] 14.1 Add tests for have method
  - [x] 14.2 Add tests for have_one_of method
  - [x] 14.3 Add tests for not_have method
  - [x] 14.4 Add tests for have_mutagen and not_have_mutagen methods
  - [x] 14.5 Add tests for all_palaces method
  - _Requirements: 4.1, 4.4_

- [x] 15. Improve test coverage for mutagen module
  - [x] 15.1 Add tests for apply_mutagen_to_palaces with different year stems
  - [x] 15.2 Add tests for edge cases in mutagen application
  - _Requirements: 4.1, 4.5_

- [x] 16. Checkpoint - Verify coverage meets 85%
  - Ensure all tests pass, ask the user if questions arise.

- [x] 17. Add missing documentation files
  - [x] 17.1 Create README_KO.md with Korean content
  - [x] 17.2 Create CONTRIBUTING.md with contribution guidelines
  - [x] 17.3 Create docs/API.md with API reference
  - _Requirements: 5.1, 5.2, 5.3_

- [x] 18. Final Checkpoint - Verify all quality checks pass
  - Ensure all tests pass, ask the user if questions arise.
