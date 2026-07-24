# DSET contract fixtures

Fixtures use two complete base changes plus deterministic case mutations from `cases.toml`. The test runner materializes each case in a temporary directory, applies only the declared mutations, and checks the expected stable diagnostic code.

The matrix covers a valid small fix, valid standard feature, valid failed/unarchived change, valid archived change, missing deterministic test plan, merged test/eval artifact, and archived change without a PR identity. Base artifacts remain human-readable examples rather than opaque generated blobs.
