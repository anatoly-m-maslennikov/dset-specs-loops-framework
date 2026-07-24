# Design — One-package project root

## Structure

```text
dset/
├── dset.toml
├── specs/packages/methodology/
│   ├── README.md
│   ├── domain.md
│   ├── spec.md
│   ├── contracts.md
│   ├── test-plan.md
│   └── eval-plan.md
├── changes/
│   ├── archive/
│   └── bootstrap-dset-project-structure/
├── templates/
└── schemas/
```

## Decisions

- `methodology` is the first explicit package because it is the only released independently meaningful capability.
- `specs/global/` is absent until at least two packages create shared contracts, end-to-end journeys, or release gates.
- `methodology/` remains the implementation/publication surface; `dset/specs/` owns accepted behavioral truth and links to that surface rather than copying the numbered documents.
- The manifest is `0.1-draft` and reports pending enforcement honestly.
- The bootstrap remained incomplete until the dated candidate on its draft PR passed the final remote-head and archive-readiness audit; it is now completed archive history.

## Future seams

Schemas, validators/utilities, and skills become new packages only when each has its own public contract and proof. Their addition may trigger `specs/global/`; this bootstrap does not decide that early.
