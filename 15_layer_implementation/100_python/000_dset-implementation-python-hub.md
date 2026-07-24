# Python methodology runtime

## Purpose

Provide the executable Python implementation of the installed DSET
methodology. The repository-root `dset_toolchain` package is the development
source; synchronization materializes the same package here in installed
methodology.

## Boundaries

This directory owns reusable execution code, not applied Decisions, QA
definitions, evidence, or Verification results. `dset_toolchain` keeps its
ecosystem-required import name inside this numbered owner.

## Start here

- `010_dset-implementation-python-run.py` — location-independent Python launcher.
- `dset_toolchain` — synchronized installed package.
