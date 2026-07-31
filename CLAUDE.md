# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

`dracor-schema` defines the TEI customization for the [DraCor](https://dracor.org) (Drama Corpora) project. A single ODD source file (`dracor.odd`) is the source of truth for three generated artifacts:

- `dist/dracor.rng` — Relax NG schema for XML validation
- `dist/dracor.sch` — ISO Schematron rules for advanced constraint checking
- `dist/index.html` — HTML encoding guidelines

## Build

```bash
./build
```

Prerequisites: Java (JDK 11+) and the `Stylesheets/` git submodule initialized:

```bash
git submodule init && git submodule update
```

The build script uses TEI XSLT Stylesheets (`Stylesheets/bin/teitoodd`, `teitorng`, `teitoschematron`, `teitohtml`) plus a custom Saxon XSLT (`html.xsl`) for HTML post-processing. Output goes to `dist/`.

## Testing

There is no automated test runner. The `tests/` directory contains XML fixtures for manual validation against the generated schema:

- Files prefixed `tst0…` are play TEI documents; most are designed to be **invalid** and test specific error conditions or Schematron rules.
- Files prefixed `tst1…` are corpus metadata files.
- `tst000000-base.xml` is the canonical **valid** base play file.

New fixtures follow the `tstNNNNNN-slug.xml` naming and continue the numeric sequence.

Validate a test file against the generated schema using an XML validator (e.g., `xmllint`, oXygen, or jing) with `dist/dracor.rng` and `dist/dracor.sch`.

**Local Schematron validation**: `xmllint --schematron` and `jing -s` cannot run these rules (XPath 2.0 + `<sch:let>`). Use a Saxon-based ISO Schematron pipeline — compile `dist/dracor.sch` with TEI's `iso_svrl_for_xslt2.xsl` and apply the resulting XSLT to a test file.

**CI**: `.github/workflows/test.yml` compile-checks the generated `dist/dracor.sch` against `tst000000-base.xml` using `schxslt-cli` on every PR touching `dracor.odd` or `tests/`.

## Migrations

XSLT stylesheets in `migrations/` update existing DraCor TEI files to the latest recommended markup. Deprecated markup remains supported until a major version change, and migrations provide the path to adopt current conventions:

```bash
./migrate.sh migrations/006-corpus-xml.xsl path/to/file.xml [more files...]
```

## Architecture

### ODD as single source

`dracor.odd` (≈7400 lines of TEI XML) contains:

- Element and attribute specifications (`<elementSpec>`, `<attDef>`)
- Prose documentation (encoding guidelines)
- Embedded Schematron rules (`<constraint>` elements) for constraints beyond what Relax NG can express — e.g., enforcing that character `@xml:id` values referenced in speech are declared in the cast list, or that specific API features are present

The build pipeline materializes these three separate concerns from the one ODD file via the TEI XSLT toolchain.

### TEI P5 / TEI Drama layering

`dracor.odd` extends the upstream TEI Drama customization with DraCor-specific constraints and narrows TEI's permissive defaults.

### Conventions for editing `dracor.odd`

- **`<constraintSpec>` placement**: insert at the top of the enclosing `<elementSpec>`, before `<attList>`/`<exemplum>`.
- **Default severity is `role="warning"`** — DraCor Schematron rules are soft encoding hints, not hard errors. Use `role="error"` only when a violation truly breaks downstream processing.
- **Cross-cutting rules** that don't belong to any single element (e.g. root-level PI checks, the empty-element rule) live on the root `TEI` `<elementSpec>`.

### Deployment

GitHub Actions workflows handle CI/CD:

- `preview.yml` — triggered by PRs touching `dracor.odd`; builds and deploys an HTML preview to `staging.dracor.org/previews/odd-{PR}.html`
- `release.yml` — triggered on GitHub release; uploads RNG/SCH/HTML as release assets and deploys to staging, dev, and production environments
- `test.yml` — Schematron compile-check on PRs (see Testing)
