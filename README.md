# DraCor Schema

This is the [ODD](https://tei-c.org/guidelines/customization/getting-started-with-p5-odds/)
of the TEI customization for the [DraCor project](https://dracor.org). It is the
source of the following resources:

- DraCor Encoding Guidelines: https://dracor.org/doc/odd
- DraCor Relax NG Schema: https://dracor.org/schema.rng
- DraCor Schematron Rules: https://dracor.org/dracor.sch

The schema files and documentation are also available as
[release assets](https://github.com/dracor-org/dracor-schema/releases).

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

The bleeding edge version of the DraCor TEI Customization and Encoding
Guidelines is published at https://dracor-org.github.io/dracor-schema/ and also
available at https://staging.dracor.org/doc/odd.

## License

The DraCor Schema is made available under the terms and conditions of the
[Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
