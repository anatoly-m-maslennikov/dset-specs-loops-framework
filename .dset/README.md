# DSET control plane

- [Project truth and records](project/README.md)
- [Settings and project manifest](dset_settings.toml)
- [Version lifecycle](versions/README.md)
- [META](meta/README.md)
- [GOV](gov/README.md)
- [TOOL](tool/README.md)
- [SKILL](skill/README.md)
- [OPS](ops/README.md)

Ignored resumable runtime state lives in the repository-root sibling
`.dset_runtime/`. Disposable process scratch lives under `/tmp` on POSIX or the
native operating-system temporary root on Windows.
