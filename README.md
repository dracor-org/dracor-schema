# dracor-schema

The TEI ODD and schema for dracor.org files.

## Getting started

```sh
git clone --recurse-submodules https://github.com/dracor-org/dracor-schema.git
cd dracor-schema
./build
ls -l dist
```

This repository uses the
[TEI XSLT Stylesheets](https://github.com/TEIC/Stylesheets) as a submodule to
build the Relax NG and Schematron schemas as well as the HTML documentation from
the ODD. After running the [build](./build) script the generated files can be
found in the `dist` directory.

## See also

The latest release of the DraCor TEI Customization and Encoding Guidelines is
published at https://dracor-org.github.io/dracor-schema/. It is also available
on the DraCor website at https://dracor.org/doc/odd.
