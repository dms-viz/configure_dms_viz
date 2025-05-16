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

## [1.0.0] - 2023-10-17

### Added

- Add a subcommand that joins together datasets into a single JSON file.

### Changed

- Breaking change that splits configure-dms-viz into to subcommads – format and join.

### Deprecated

- N/A

### Removed

- N/A

## [1.1.0] - 2023-10-17

### Added

- Add the ability to include a 'chain' column in the sitemap to support discontinuous sites.

### Changed

- N/A

### Deprecated

- N/A

### Removed

- N/A

## [1.1.1] - 2023-11-03

### Added

- Add the ability to specify a default value for the filter sliders.

### Changed

- N/A

### Deprecated

- N/A

### Removed

- N/A

## [1.2.0] - 2024-02-13

### Added

- N/A

### Changed

- It's now possible to include `protein_sites` proceed by insertion codes like (i.e. 52A, 214B, etc...). Previously, `protein_sites` could only be numeric and non-numeric sites were ignored by the `dms-viz`.

### Deprecated

- N/A

### Removed

- N/A

## [1.2.0] - 2024-03-01

### Added

- Added a warning to `join` if two `json` datasets have the name top-level key/name.

### Changed

- N/A

### Deprecated

- N/A

### Removed

- N/A

## [1.2.2] - 2024-03-29

### Added

- Don't allow white space or empty strings for included/excluded chains.

### Changed

- N/A

### Deprecated

- N/A

### Removed

- N/A

## [1.3.0] - 2024-04-02

### Added

- N/A

### Changed

- Sitemaps are now optional. If you do not provide one, all sites are sequential and the reference sites in your input data are the same as the protein sites.

### Deprecated

- N/A

### Removed

- N/A

## [1.3.1] - 2024-04-02

### Added

- N/A

### Changed

- When checking the protein structure, don't include site with non-matching wildtype resides as "missing".

### Deprecated

- N/A

### Removed

- N/A

## [1.3.2] - 2024-04-02

### Added

- N/A

### Changed

- Fix a bug where `protein` sites aren't properly mapped to the structure if they're of type `Float`.

### Deprecated

- N/A

### Removed

- N/A

## [1.3.3] - 2024-04-24

### Added

- Throw an error if the same chains are present in `included` and `excluded` chain lists

### Changed

- N/A

### Deprecated

- N/A

### Removed

- N/A

## [1.3.4] - 2024-05-15

### Added

- N/A

### Changed

- Fixes a bug where the markdown description was included in the count of keys compared to the number of input files causing the join command to exit before completing.

### Deprecated

- N/A

### Removed

- N/A

## [1.4.0] - 2024-05-16

### Added

- Added a flag (--heatmap-limits) to allow users to set the limits of the color scale.
- Added a human dataset (PTEN VAMPseq)
- Attempt to sort the reference sites when no sitemap is provided

### Changed

- N/A

### Deprecated

- N/A

### Removed

- N/A

## [1.5.0] - 2024-05-20

### Added

- Added a flag (--summary-stat) to allow users to set the default summary metric
- Added a flag (--floor) to allow users to set whether the data is floor by default

### Changed

- N/A

### Deprecated

- N/A

### Removed

- N/A

## [1.6.0] - 2024-11-25

### Added

- N/A

### Changed

- Sort the keys in the output JSON to prevent overhead in `git` diffs. 

### Deprecated

- N/A

### Removed

- N/A

## [1.7.0] - 2025-05-16

### Added

- N/A

### Changed

- Sort the condition column values in the output JSON to prevent overhead in `git` diffs. 

### Deprecated

- N/A

### Removed

- N/A