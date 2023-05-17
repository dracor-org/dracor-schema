"""Dummy flask API to generate the OpenAPI Specification
including the schemas in dracor_api_response_schemas.py"""

import flask
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
import json
from dracor_api_response_schemas import InfoSchema, CorpusInCorporaSchema, CorpusSchema, \
    PlayMetadataSchema, PlaySchema, PlayMetricsSchema, CastItemSchema, SpokenTextByCharacterSchema, \
    PlayWithWikidataCharacterSchema


# Setup of flask API
api = flask.Flask(__name__)
# enable UTF-8 support
api.config["JSON_AS_ASCII"] = False


@api.route("/info", methods=["GET"])
def get_info():
    """
    ---
    get:
      summary: API info
      description: >-
        Shows version numbers of the dracor-api app and the underlying
        eXist-db.
      operationId: api-info
      tags: [public]
      responses:
        '200':
          description: Returns JSON object
          content:
            application/json:
                schema: InfoSchema
    """
    pass


@api.route("/corpora", methods=["GET"])
def get_corpora():
    """
    ---
    get:
      summary: List available corpora
      operationId: list-corpora
      tags: [public]
      parameters:
        -   name: include
            in: query
            description: Include metrics for each corpus
            required: false
            schema:
                type: string
                enum: [metrics]
      responses:
        '200':
          description: Returns list of available corpora
          content:
            application/json:
              schema:
                type: array
                items: CorpusInCorporaSchema
    """
    pass


@api.route("/corpora/<path:corpus_name>", methods=["GET"])
def list_corpus_content(corpus_name: str):
    """
    ---
    get:
        summary: List corpus content
        description: >-
            Lists all plays available in the corpus including the id, title,
            author(s) and other meta data.
            operationId: list-corpus-content
        tags: [public]
        parameters:
            -   name: corpusname
                in: path
                required: true
                description: >
                    Short name of the corpus as provided in the `name` property of the result
                    objects from the [/corpora](#/public/list-corpora) endpoint
                schema:
                    type: string
                examples:
                    GerDraCor:
                        value: ger
                        summary: German Drama Corpus
                    GreekDraCor:
                        value: greek
                        summary: Greek Drama Corpus
                    ItaDraCor:
                        value: ita
                        summary: Italian Drama Corpus
                    RomDraCor:
                        value: rom
                        summary: Roman Drama Corpus
                    RusDraCor:
                        value: rus
                        summary: Russian Drama Corpus
                    ShakeDraCor:
                        value: shake
                        summary: Shakespeare Drama Corpus
                    SpanDraCor:
                        value: span
                        summary: Spanish Drama Corpus
        responses:
            '200':
                description: Returns object representing corpus contents
                content:
                    application/json:
                        schema: CorpusSchema
            '404':
                description: Corpus not found
    """
    pass


@api.route("/corpora/<path:corpus_name>/metadata", methods=["GET"])
def get_corpus_plays_metadata(corpus_name: str):
    """
    ---
    get:
        summary: List of metadata for all plays in a corpus
        operationId: corpus-metadata
        tags: [public]
        parameters:
            -   name: corpusname
                in: path
                required: true
                description: >
                    Short name of the corpus as provided in the `name` property of the result
                    objects from the [/corpora](#/public/list-corpora) endpoint
                schema:
                    type: string
                examples:
                    GerDraCor:
                        value: ger
                        summary: German Drama Corpus
                    GreekDraCor:
                        value: greek
                        summary: Greek Drama Corpus
                    ItaDraCor:
                        value: ita
                        summary: Italian Drama Corpus
                    RomDraCor:
                        value: rom
                        summary: Roman Drama Corpus
                    RusDraCor:
                        value: rus
                        summary: Russian Drama Corpus
                    ShakeDraCor:
                        value: shake
                        summary: Shakespeare Drama Corpus
                    SpanDraCor:
                        value: span
                        summary: Spanish Drama Corpus
        responses:
            '200':
                description: Returns a list of metadata for all plays
                content:
                    application/json:
                        schema:
                            type: array
                            items: PlayMetadataSchema
            text/csv:
              schema:
                type: string
    """
    pass


@api.route("/corpora/<path:corpus_name>/play/<path:play_name>", methods=["GET"])
def get_play(corpus_name: str, play_name: str):
    """
    ---
    get:
        summary: Get metadata and network metrics for a single play
        operationId: play-info
        tags: [public]
        parameters:
            -   name: corpusname
                in: path
                required: true
                description: >
                    Short name of the corpus as provided in the `name` property of the result
                    objects from the [/corpora](#/public/list-corpora) endpoint
                schema:
                    type: string
                examples:
                    GerDraCor:
                        value: ger
                        summary: German Drama Corpus
                    GreekDraCor:
                        value: greek
                        summary: Greek Drama Corpus
                    ItaDraCor:
                        value: ita
                        summary: Italian Drama Corpus
                    RomDraCor:
                        value: rom
                        summary: Roman Drama Corpus
                    RusDraCor:
                        value: rus
                        summary: Russian Drama Corpus
                    ShakeDraCor:
                        value: shake
                        summary: Shakespeare Drama Corpus
                    SpanDraCor:
                        value: span
                        summary: Spanish Drama Corpus

            -   name: playname
                in: path
                required: true
                description: >
                    Name parameter (or "slug") of the play as provided in the `name`
                    property of the result objects of the
                    [/corpora/{corpusname}](#/public/list-corpus-content) endpoint.
                schema:
                    type: string
                examples:
                    lessing_galotti:
                        value: lessing-emilia-galotti
                        summary: "G.E. Lessing: Emilia Galotti (GerDraCor)"
                    aeschylus_persians:
                        value: aeschylus-persians
                        summary: "Aeschylus: Persians (GreekDraCor)"
                    goldoni_servitore:
                        value: goldoni-il-servitore-di-due-padroni
                        summary: "C. Goldoni: Il servitore di due padroni (ItaDraCor)"
                    seneca_medea:
                        value: seneca-medea
                        summary: "Seneca: Medea (RomDraCor)"
                    gogol_revizor:
                        value: gogol-revizor
                        summary: "N. Gogol: Revizor (RusDraCor)"
                    shakespeare_hamlet:
                        value: hamlet
                        summary: "W. Shakespeare: Hamlet (ShakeDraCor)"
                    munoz_refugio:
                        value: munoz-refugio
                        summary: "P. Muñoz Seca: El Refugio (SpanDraCor)"
        responses:
            '200':
                description: Returns an object with play meta data
                content:
                    application/json:
                        schema: PlaySchema
    """
    pass


@api.route("/corpora/<path:corpus_name>/play/<path:play_name>/metrics", methods=["GET"])
def get_play_metrics(corpus_name: str, play_name: str):
    """
    ---
    get:
        summary: Get network metrics for a single play
        operationId: play-metrics
        tags: [public]
        parameters:
            -   name: corpusname
                in: path
                required: true
                description: >
                    Short name of the corpus as provided in the `name` property of the result
                    objects from the [/corpora](#/public/list-corpora) endpoint
                schema:
                    type: string
                examples:
                    GerDraCor:
                        value: ger
                        summary: German Drama Corpus
                    GreekDraCor:
                        value: greek
                        summary: Greek Drama Corpus
                    ItaDraCor:
                        value: ita
                        summary: Italian Drama Corpus
                    RomDraCor:
                        value: rom
                        summary: Roman Drama Corpus
                    RusDraCor:
                        value: rus
                        summary: Russian Drama Corpus
                    ShakeDraCor:
                        value: shake
                        summary: Shakespeare Drama Corpus
                    SpanDraCor:
                        value: span
                        summary: Spanish Drama Corpus
            -   name: playname
                in: path
                required: true
                description: >
                    Name parameter (or "slug") of the play as provided in the `name`
                    property of the result objects of the
                    [/corpora/{corpusname}](#/public/list-corpus-content) endpoint.
                schema:
                    type: string
                examples:
                    lessing_galotti:
                        value: lessing-emilia-galotti
                        summary: "G.E. Lessing: Emilia Galotti (GerDraCor)"
                    aeschylus_persians:
                        value: aeschylus-persians
                        summary: "Aeschylus: Persians (GreekDraCor)"
                    goldoni_servitore:
                        value: goldoni-il-servitore-di-due-padroni
                        summary: "C. Goldoni: Il servitore di due padroni (ItaDraCor)"
                    seneca_medea:
                        value: seneca-medea
                        summary: "Seneca: Medea (RomDraCor)"
                    gogol_revizor:
                        value: gogol-revizor
                        summary: "N. Gogol: Revizor (RusDraCor)"
                    shakespeare_hamlet:
                        value: hamlet
                        summary: "W. Shakespeare: Hamlet (ShakeDraCor)"
                    munoz_refugio:
                        value: munoz-refugio
                        summary: "P. Muñoz Seca: El Refugio (SpanDraCor)"
        responses:
            '200':
                description: Returns an object with metrics data
                content:
                    application/json:
                        schema: PlayMetricsSchema
    """
    pass


@api.route("/corpora/<path:corpus_name>/play/<path:play_name>/cast", methods=["GET"])
def get_play_cast(corpus_name: str, play_name: str):
    """
    ---
    get:
        summary: Get a list of characters of a play
        operationId: get-cast
        tags: [public]
        parameters:
            -   name: corpusname
                in: path
                required: true
                description: >
                    Short name of the corpus as provided in the `name` property of the result
                    objects from the [/corpora](#/public/list-corpora) endpoint
                schema:
                    type: string
                examples:
                    GerDraCor:
                        value: ger
                        summary: German Drama Corpus
                    GreekDraCor:
                        value: greek
                        summary: Greek Drama Corpus
                    ItaDraCor:
                        value: ita
                        summary: Italian Drama Corpus
                    RomDraCor:
                        value: rom
                        summary: Roman Drama Corpus
                    RusDraCor:
                        value: rus
                        summary: Russian Drama Corpus
                    ShakeDraCor:
                        value: shake
                        summary: Shakespeare Drama Corpus
                    SpanDraCor:
                        value: span
                        summary: Spanish Drama Corpus
            -   name: playname
                in: path
                required: true
                description: >
                    Name parameter (or "slug") of the play as provided in the `name`
                    property of the result objects of the
                    [/corpora/{corpusname}](#/public/list-corpus-content) endpoint.
                schema:
                    type: string
                examples:
                    lessing_galotti:
                        value: lessing-emilia-galotti
                        summary: "G.E. Lessing: Emilia Galotti (GerDraCor)"
                    aeschylus_persians:
                        value: aeschylus-persians
                        summary: "Aeschylus: Persians (GreekDraCor)"
                    goldoni_servitore:
                        value: goldoni-il-servitore-di-due-padroni
                        summary: "C. Goldoni: Il servitore di due padroni (ItaDraCor)"
                    seneca_medea:
                        value: seneca-medea
                        summary: "Seneca: Medea (RomDraCor)"
                    gogol_revizor:
                        value: gogol-revizor
                        summary: "N. Gogol: Revizor (RusDraCor)"
                    shakespeare_hamlet:
                        value: hamlet
                        summary: "W. Shakespeare: Hamlet (ShakeDraCor)"
                    munoz_refugio:
                        value: munoz-refugio
                        summary: "P. Muñoz Seca: El Refugio (SpanDraCor)"
        responses:
            '200':
                description: Returns list of characters
                content:
                    application/json:
                        schema:
                            type: array
                            items: CastItemSchema
                    text/csv:
                        schema:
                            type: string
    """
    pass


@api.route("/corpora/<path:corpus_name>/play/<path:play_name>/spoken-text-by-character", methods=["GET"])
def get_spoken_text_by_character(corpus_name: str, play_name: str):
    """
    ---
    get:
        summary: Get spoken text for each character of a play
        operationId: play-spoken-text-by-character
        tags: [public]
        parameters:
            -   name: corpusname
                in: path
                required: true
                description: >
                    Short name of the corpus as provided in the `name` property of the result
                    objects from the [/corpora](#/public/list-corpora) endpoint
                schema:
                    type: string
                examples:
                    GerDraCor:
                        value: ger
                        summary: German Drama Corpus
                    GreekDraCor:
                        value: greek
                        summary: Greek Drama Corpus
                    ItaDraCor:
                        value: ita
                        summary: Italian Drama Corpus
                    RomDraCor:
                        value: rom
                        summary: Roman Drama Corpus
                    RusDraCor:
                        value: rus
                        summary: Russian Drama Corpus
                    ShakeDraCor:
                        value: shake
                        summary: Shakespeare Drama Corpus
                    SpanDraCor:
                        value: span
                        summary: Spanish Drama Corpus
            -   name: playname
                in: path
                required: true
                description: >
                    Name parameter (or "slug") of the play as provided in the `name`
                    property of the result objects of the
                    [/corpora/{corpusname}](#/public/list-corpus-content) endpoint.
                schema:
                    type: string
                examples:
                    lessing_galotti:
                        value: lessing-emilia-galotti
                        summary: "G.E. Lessing: Emilia Galotti (GerDraCor)"
                    aeschylus_persians:
                        value: aeschylus-persians
                        summary: "Aeschylus: Persians (GreekDraCor)"
                    goldoni_servitore:
                        value: goldoni-il-servitore-di-due-padroni
                        summary: "C. Goldoni: Il servitore di due padroni (ItaDraCor)"
                    seneca_medea:
                        value: seneca-medea
                        summary: "Seneca: Medea (RomDraCor)"
                    gogol_revizor:
                        value: gogol-revizor
                        summary: "N. Gogol: Revizor (RusDraCor)"
                    shakespeare_hamlet:
                        value: hamlet
                        summary: "W. Shakespeare: Hamlet (ShakeDraCor)"
                    munoz_refugio:
                        value: munoz-refugio
                        summary: "P. Muñoz Seca: El Refugio (SpanDraCor)"
        responses:
            '200':
                description: Returns texts per character
                content:
                    application/json:
                        schema:
                            type: array
                            items: SpokenTextByCharacterSchema

                    text/csv:
                        schema:
                            type: string
    """
    pass


@api.route("/character/<path:character_wd>", methods=["GET"])
def get_plays_with_wikidata_character(character_wd: str):
    """
    ---
    get:
        summary: List plays having a character identified by Wikidata ID
        operationId: plays-with-character
        tags: [public]
        parameters:
            -   name: id
                in: path
                required: true
                schema:
                    type: string
                    example: Q131412
        responses:
            '200':
                description: List of plays.
                content:
                    application/json:
                        schema:
                            type: array
                            items: PlayWithWikidataCharacterSchema

            '400':
                description: Invalid character ID.
    """
    pass


spec = APISpec(
    title="DraCor API",
    version="0.83.1",
    openapi_version="3.0.3",
    info=dict(
        contact=dict(
            email="fr.fischer@fu-berlin.de"
        ),
        termsOfService = "https://dracor.org",
        license=dict(
            name="Apache 2.0",
            url="http://www.apache.org/licenses/LICENSE-2.0.html"
        )
    ),
    servers=[
        dict(
            description="Production",
            url="https://dracor.org/api"
        )
    ],
    plugins=[FlaskPlugin(), MarshmallowPlugin()]
)

# Generate the OpenAPI Specification
with api.test_request_context():
    spec.path(view=get_info)
    spec.path(view=get_corpora)
    spec.path(view=list_corpus_content)
    spec.path(view=get_corpus_plays_metadata)
    spec.path(view=get_play)
    spec.path(view=get_play_metrics)
    spec.path(view=get_play_cast)
    spec.path(view=get_spoken_text_by_character)
    spec.path(view=get_plays_with_wikidata_character)


# write the OpenAPI Specification as YAML to the root folder
with open('dracor_api_openapi.yaml', 'w') as f:
    f.write(spec.to_yaml())

# Write the Specification as JSON to the root folder
with open('dracor_api_openapi.json', 'w') as f:
    json.dump(spec.to_dict(), f)

