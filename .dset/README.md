# DSET control plane

- [Project truth and records](project/README.md)
- [Settings and project manifest](dset_settings.toml)
- [Version lifecycle](versions/README.md)
- [META](layer_1_meta/README.md)
- [GOV](layer_2_gov/README.md)
- [TOOL](layer_3_tool/README.md)
- [SKILL](layer_4_skill/README.md)
- [OPS](layer_5_ops/README.md)

Ignored resumable runtime state lives in the repository-root sibling
`.dset_runtime/`. Disposable process scratch lives under `/tmp` on POSIX or the
native operating-system temporary root on Windows.
