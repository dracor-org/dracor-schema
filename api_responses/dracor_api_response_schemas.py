"""Marshmallow Schemas of DraCor API response objects

Used current production version (v0.89.0).

"""
from marshmallow import Schema, fields, ValidationError
import logging


# Function to do the validation
def is_valid(item: dict, schema: Schema, catch_error: bool = True) -> bool:
    """Helper function to validate labels

    Args:
    item (dict): Item to validate
    schema (Schema): Schema used to validate
    catch_error (bool): Catch the ValidationError exception. Defaults to True

    Returns:
        bool: True if valid
    """
    schema_instance = schema()
    if catch_error:
        try:
            schema_instance.load(item)
            logging.info("Validation passed.")
            return True
        except ValidationError:
            logging.info("Validation failed.")
            return False
    else:
        # errors are not caught
        schema_instance.load(item)


# /info endpoint
class InfoSchema(Schema):
    """Response object of the /info endpoint"""
    name = fields.Str()
    status = fields.Str()
    version = fields.Str()
    existdb = fields.Str()


# /corpora endpoint
class WordCountsSchema(Schema):
    """Counts of Word Tokens embedded in the metrics object included in the response of the /corpora endpoint"""
    # C16 corpus_num_of_word_tokens_in_text_elements
    text = fields.Int()
    # C17 corpus_num_of_word_tokens_in_sp
    sp = fields.Int()
    # C18 corpus_num_of_word_tokens_in_stage
    stage = fields.Int()


class CorpusMetricsSchema(Schema):
    """Metrics object included in the corpus object returned by the /corpora endpoint"""
    # C9 corpus_num_of_plays
    plays = fields.Int()
    # C10 corpus_num_of_characters
    characters = fields.Int()
    # C11 corpus_num_of_characters_male
    male = fields.Int()
    # C12 corpus_num_of_characters_female
    female = fields.Int()
    # C13 corpus_num_of_tei_text_elements
    text = fields.Int()
    # C14 corpus_num_of_sp
    sp = fields.Int()
    # C15 corpus_num_of_stage
    stage = fields.Int()
    # Counts of words
    wordcount = fields.Nested(WordCountsSchema)
    # C19 corpus_metrics_date_updated
    updated = fields.Str()


class CorpusInCorporaSchema(Schema):
    """Single corpus object in the response of the /corpora endpoint"""
    # C1 corpus_name:
    name = fields.Str()
    # C2 corpus_uri:
    uri = fields.Url()
    # C3 corpus_title
    title = fields.Str()
    # C4 corpus_acronym
    acronym = fields.Str()
    # C5 corpus_description
    description = fields.Str()
    # C6 corpus_repository
    repository = fields.Url()
    # C7 corpus_licence
    licence = fields.Str()
    # C8 corpus_licence_url
    licenceUrl = fields.Url()
    # depending on include parameter, if set to "metrics":
    metrics = fields.Nested(CorpusMetricsSchema, required=False)

# /corpora/{corpusname} endpoint


class FirstAuthorInPlayInCorpusSchema(Schema):
    """(Deprecated) Single/First Author Object in a Play Object in the response of the /corpora/{corpusname} endpoint"""
    # P15 play_first_author_name
    name = fields.Str()


class ExternalReferenceResourceIdSchema(Schema):
    """ID in an external reference resource as included for example in the author object in a play in the
    response of the /corpora/{corpusname} endpoint"""
    ref = fields.Str()
    type = fields.Str()


class AuthorInPlayInCorpusSchema(Schema):
    """Author in list of authors in a play object in the response of the /corpora/{corpusname} endpoint"""
    # P9 play_author_name
    name = fields.Str()
    # P10 play_author_name_en
    nameEn = fields.Str(required=False)
    # P11 play_author_fullname
    fullname = fields.Str()
    # P12 play_author_fullname_en
    fullnameEn = fields.Str(required=False)
    # P13 play_author_shortname
    shortname = fields.Str()
    # P14 play_author_shortname_en
    shortnameEn = fields.Str(required=False)
    # P18 play_author_also_known_as (unlike in the Table in the report this key can be found in the response)
    alsoKnownAs = fields.List(fields.Str(), required=False)
    # IDs in external reference resources
    refs = fields.List(fields.Nested(ExternalReferenceResourceIdSchema))


class PlayInCorpusSchema(Schema):
    """Play object as contained in the response of the /corpora/{corpusname} endpoint"""
    # P2 play_id
    id = fields.Str()
    # P3 play_name
    name = fields.Str()
    # P4 play_wikidata_id
    # e.g. in cal this information is not available
    wikidataId = fields.Str(allow_none=True)
    # P5 play_title
    title = fields.Str()
    # P6 play_subtitle
    subtitle = fields.Str()
    # P7 play_title_en
    titleEn = fields.Str(required=False)
    # P8 play_subtitle_en
    subtitleEn = fields.Str(required=False)

    # There are still some issues with the fields for the years
    # see also issue https://github.com/dracor-org/dracor-api/issues/186

    # P24 play_year_written; this was changed from "writtenYear" to "yearWritten" after finishing the report
    # This field can be also JSON null, gues that this would be None in Python
    # strangely, per default, the values are string, whereas yearNormalized is of type integer
    # If native "allow_none" does not work, maybe solution for an UnionField is here
    yearWritten = fields.Str(allow_none=True)
    # P25 play_year_printed; this was changed from "printYear" to "yearPrinted" after finishing the report (see above)
    yearPrinted = fields.Str(allow_none=True)
    # P26 play_year_premiered; this was changed from "premiereYear" to "yearPremiered" after finishing
    yearPremiered = fields.Str(allow_none=True)
    # P27 play_year_normalized
    yearNormalized = fields.Int(allow_none=True)

    # as per 2023-05-09 the deprecated keys "writtenYear", "printYear", "premiereYear" are still in the response
    # they seem to return the years as string
    # the fields are kept as optional for now
    # TODO: implement function to check if they are still there
    writtenYear = fields.Str(allow_none=True, required=False)
    printYear = fields.Str(allow_none=True, required=False)
    premiereYear = fields.Str(allow_none=True, required=False)

    # P28 play_digital_source_name
    # in cal this can be an empty string
    source = fields.Str(allow_none=True)
    # P29 play_digital_source_url
    # in cal: if url is not available an empty string is returned; Validation as URL is not possible
    # set this to string for now
    # sourceUrl = fields.Url(allow_none=True)
    # TODO: change this back here
    sourceUrl = fields.Str(allow_none=True)
    # P53 play_network_data_csv_url
    networkdataCsvUrl = fields.Url()
    # P55 play_network_size
    networkSize = fields.Int()

    # Author data; deprecated single/first author
    author = fields.Nested(FirstAuthorInPlayInCorpusSchema)
    # all authors in an list / JSON array
    authors = fields.List(fields.Nested(AuthorInPlayInCorpusSchema))


class CorpusSchema(Schema):
    """Response Object returned by the /corpora/{corpusname} endpoint"""
    # C1 corpus_name:
    name = fields.Str()
    # C3 corpus_title
    title = fields.Str()
    # C4 corpus_acronym
    acronym = fields.Str()
    # C5 corpus_description
    description = fields.Str()
    # C6 corpus_repository
    repository = fields.Url()
    # C7 corpus_licence
    licence = fields.Str()
    # C8 corpus_licence_url
    licenceUrl = fields.Url()
    # C20 corpus_play_objects
    dramas = fields.List(fields.Nested(PlayInCorpusSchema))


# characterGender = fields.Str(validate=validate.OneOf(["male", "female", "nonbinary"]))


