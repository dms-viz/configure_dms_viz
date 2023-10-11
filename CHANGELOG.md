# `configure_dms_viz` Changelog

## [0.1.0] - 2023-08-01

### Added

- Initial release of the `configure_dms_viz` project.

### Changed

- N/A (This is the first release)

### Deprecated

- N/A (This is the first release)

### Removed

- N/A (This is the first release)

## [0.2.0] - 2023-08-28

### Added

- Make it possible to choose the colors on the negative color scale for each condition.

### Changed

- N/A

### Deprecated

- N/A

### Removed

- N/A

## [0.3.0] - 2023-08-29

### Added

- Make it possible to choose the colors on the negative color scale for each condition.

### Changed

- Fixed a bug where the filter columns were used for both filter and tooltip columns regardless of user input.

### Deprecated

- N/A

### Removed

- N/A

## [0.3.1] - 2023-09-05

### Added

- N/A

### Changed

- Fixed a bug that occurs if `NaN` values are found in the `metric` column. If `NaN` is present the visualization tool records these is 'observed' but 'filtered' due to the way `NaN` values are handled by the visualization. There is no reason to have measurements with `NaN` in the metric column, so these are filtered out and the user is warned about their presence.

### Deprecated

- N/A

### Removed

- N/A

## [0.3.2] - 2023-09-15

### Added

- Added tests/examples for three new datasets:
  1. Caelan's HIV DMS data
  2. Jesse's SARS-CoV-2 mutation fitness data
  3. The Lauring lab's IAV PB1 DMS data
- Configured the tests with `pytest`

### Changed

- N/A

### Deprecated

- N/A

### Removed

- N/A

## [0.3.3] - 2023-09-15

### Added

- Add SARS-CoV-2 RBD antibody escape example
- Filter out sites that don't have any mutations

### Changed

- Updated the descriptions for each test/example

### Deprecated

- N/A

### Removed

- N/A
