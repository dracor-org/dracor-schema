"""Marshmallow Schemas of DraCor API response objects

Used current production version (v0.89.0).

"""
from marshmallow import Schema, fields, validate, ValidationError
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


# Field that can hold values of multiple types; this is a mess!
class StringOrListOfStringsField(fields.Field):
    """Field that can hold a value of type string or a list or be of None type
    solution taken from https://stackoverflow.com/questions/61614546/python-marshmallow-field-can-be-two-different-types
    """
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, str) or isinstance(value, list):
            return value
        else:
            raise ValidationError('Field should be str or list')


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


# /corpora/{corpusname}/metadata

"""
{
    "id": "ger000569",
    "name": "adolph-am-ersten-mai",
    "playName": "adolph-am-ersten-mai",
    "wikidataId": "Q111795417",
    "normalizedGenre": null,
    "libretto": false,
    "firstAuthor": "Adolph",
    "title": "Am ersten Mai",
    "subtitle": "Eine Tragikomödie der Arbeit aus Friedenstagen",
    "numOfCoAuthors": 0,
    "maxDegreeIds": "mieter",
    "numOfSegments": 18,
    "numOfActs": 0,
    "numOfSpeakers": 7,
    "numOfSpeakersMale": 5,
    "numOfSpeakersFemale": 2,
    "numOfSpeakersUnknown": 0,
    "numOfPersonGroups": 0,
    "numOfP": 244,
    "numOfL": 2,
    "wikipediaLinkCount": 0,
    "wordCountText": 7696,
    "wordCountSp": 7438,
    "wordCountStage": 998,
    "yearWritten": null,
    "yearPremiered": "1920",
    "yearPrinted": "1919",
    "yearNormalized": 1919,
    "digitalSource": "https://www.projekt-gutenberg.org/adolph/am1mai/index.html",
    "originalSourcePublisher": null,
    "originalSourcePubPlace": null,
    "originalSourceYear": null,
    "originalSourceNumberOfPages": null,
    "averageDegree": 3.7142857142857144,
    "density": 0.6190476190476191,
    "averageClustering": 0.738095238095238,
    "size": 7,
    "maxDegree": 6,
    "numConnectedComponents": 1,
    "numEdges": 13,
    "diameter": 2,
    "averagePathLength": 1.380952380952381
  }
"""


class PlayMetadataSchema(Schema):
    """Play metadata object returned in the response of the /corpora/{corpusname}/metadata endpoint"""
    # P2 play_id
    id = fields.Str()
    # P3 play_name (duplicates "name" and "playName")
    name = fields.Str()
    playName = fields.Str()
    # P4 play_wikidata_id
    wikidataId = fields.Str(allow_none=True)
    # P5 play_title
    title = fields.Str()
    # P6 play_subtitle
    subtitle = fields.Str(allow_none=True)
    # P16 play_first_author_shortname
    firstAuthor = fields.Str()
    # P21 play_num_of_co_authors
    numOfCoAuthors = fields.Int()
    # P22 play_genre_normalized
    normalizedGenre = fields.Str(allow_none=True)
    # P23 play_is_libretto
    libretto = fields.Bool()
    # P24 play_year_written
    yearWritten = fields.Str(allow_none=True)
    # P25 play_year_printed
    yearPrinted = fields.Str(allow_none=True)
    # P26 play_year_premiered
    yearPremiered = fields.Str(allow_none=True)
    # P27 play_year_normalized
    yearNormalized = fields.Int(allow_none=True)
    # P29 play_digital_source_url
    # In FreDraCor: ValidationError: {'digitalSource': ['Not a valid URL.']}
    # This is the same problem as in "PlayInCorpusSchema" because of empty string?
    # TODO: revert back to url later?!
    # digitalSource = fields.Url(allow_none=True)
    # digitalSource = fields.Str(allow_none=True)
    # also produces a ValidationError: {'digitalSource': ['Not a valid string.']}
    # because FreDraCor outputs an array
    # "digitalSource": [
    #       "http://theatre-classique.fr/pages/programmes/edition.php?t=../documents/ABEILLE_ARGELIE.xml",
    #       "http://theatre-classique.fr/pages/documents/ABEILLE_ARGELIE.xml"
    #     ]
    # This is a hack with a custom field: This is nor perfect, because actually, it should check if the value is a URL.
    digitalSource = StringOrListOfStringsField(allow_none=True)
    # P31 play_original_source_publisher
    originalSourcePublisher = fields.Str(allow_none=True)
    # P32 play_original_source_publication_place
    originalSourcePubPlace = fields.Str(allow_none=True)
    # P33 play_original_source_publication_year
    originalSourceYear = fields.Int(allow_none=True)
    # P34 play_original_source_num_of_pages
    originalSourceNumberOfPages = fields.Int(allow_none=True)
    # P35 play_num_of_wikipedia_links
    wikipediaLinkCount = fields.Int(allow_none=True)
    # P37 play_num_of_segments
    numOfSegments = fields.Int()
    # P38 play_num_of_acts
    numOfActs = fields.Int()
    # P39 play_num_of_paragraphs
    numOfP = fields.Int()
    # P40 play_num_of_verse_lines
    numOfL = fields.Int()
    # P41 play_num_of_word_tokens_in_text_elements
    wordCountText = fields.Int()
    # P42 play_num_of_word_tokens_in_sp
    wordCountSp = fields.Int()
    # P43 play_num_of_word_tokens_in_stage
    wordCountStage = fields.Int()
    # P45 play_num_of_speakers
    numOfSpeakers = fields.Int()
    # P46 play_num_of_speakers_gender_female
    numOfSpeakersFemale = fields.Int()
    # P47 play_num_of_speakers_gender_male
    numOfSpeakersMale = fields.Int()
    # P48 play_num_of_speakers_gender_unknown
    numOfSpeakersUnknown = fields.Int()
    # P49 play_num_of_person_groups
    numOfPersonGroups = fields.Int()
    # P55 play_network_size
    size = fields.Int()
    # P56 play_network_num_of_edges
    numEdges = fields.Int()
    # P57 play_network_average_degree
    averageDegree = fields.Float()
    # P58 play_network_density
    density = fields.Float()
    # P59 play_network_diameter
    diameter = fields.Int()
    # P60 play_network_average_path_length
    averagePathLength = fields.Float()
    # P61 play_network_average_clustering
    averageClustering = fields.Float()
    # P62 play_network_num_connected_components
    numConnectedComponents = fields.Int()
    # P63 play_network_max_degree
    maxDegree = fields.Int()
    # P46 play_network_max_degree_character_ids
    maxDegreeIds = fields.Str()

# /corpus/{corpusname}/play/{playname}

class AuthorInPlayMetadataSchema(Schema):
    """Author Object in the object returned by the /corpora/{corpusname}/play/{playname}"""
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
    shortnameEn = fields.Str()
    # P18 play_author_also_known_as
    alsoKnownAs = fields.List(fields.Str(), required=False)
    # IDs in External Reference Resources
    refs = fields.List(fields.Nested(ExternalReferenceResourceIdSchema))


class FirstAuthorInPlayMetadataSchema(Schema):
    """(Deprecated) First Author Object in PlayMetadataSchema"""
    # P15 play_first_author_name
    name = fields.Str()
    # P17 play_first_author_deprecation_warning
    warning = fields.Str(
        validate=validate.Equal("The single author property is deprecated. Use the array of 'authors' instead!"))


class SourceInPlayMetadataSchema(Schema):
    """Source object included in the play metadata object returned by the /corpora/{corpusname}/play/{playname}
    endpoint"""
    # P28 play_digital_source_name
    # HunDraCor has plays w/o this value
    name = fields.Str(allow_none=True)
    # P29 play_digital_source_url
    # url = fields.Url()
    # This is a hack because of CalDraCor
    # TODO: revert that back to URL
    url = StringOrListOfStringsField(allow_none=True)


class CastItemInPlayMetadataSchema(Schema):
    """Character data as included in the response object of the /corpora/{corpusname}/play/{playname} endpoint"""
    # Ch1 character_id
    id = fields.Str()
    # Ch2 character_name
    # In CalDraCor this can be None/null
    name = fields.Str(allow_none=True)
    # Ch3 character_is_group
    isGroup = fields.Bool()
    # Ch4 character_gender
    # In CalDraCor this can be null/None
    # CalDraCor has "DIVERSE" for some obscure reason
    # Change below, if CalDraCor must be validated, this is no fun anyway.
    sex = fields.Str(validate=validate.OneOf(["MALE", "FEMALE", "UNKNOWN"]), allow_none=True)
    # sex = fields.Str(validate=validate.OneOf(["MALE", "FEMALE", "UNKNOWN", "DIVERSE"]), allow_none=True)
    # Ch5 character_wikidata_id
    wikidataId = fields.Str(required=False)


class SegmentItemInPlayMetadataSchema(Schema):
    """Segment data as included in the response object of the /corporoa/{corpusname}/play/{playname} endpoint"""
    # S1 segment_type
    # in CalDraCor this can be null/None
    # TODO: maybe disallow None/null?
    type = fields.Str(allow_none=True)
    # S2 segment_number
    number = fields.Int()
    # S3 segment_title
    title = fields.Str()
    # S4 segment_speaking_characters
    speakers = fields.List(fields.Str())


class RelationItemInPlayMetadataSchema(Schema):
    """Relation data as included in the response object of the /corporoa/{corpusname}/play/{playname} endpoint"""
    # No features have been defined for a relation; relations in general are P52 play_character_relations
    directed = fields.Bool()
    # Values see ODD
    # https://github.com/dracor-org/dracor-schema/blob/a6e5b26f7156557cc460e16a75c5e274d2775f5b/odd/dracor.odd#L4600-L4631
    type = fields.Str(validate=validate.OneOf(["parent_of", "lover_of", "related_with", "associated_with",
                                               "siblings", "spouses", "friends"]))
    source = fields.Str()
    target = fields.Str()


class PlaySchema(Schema):
    """Response Object returned by the /corpora/{corpusname}/play/{playname} endpoint"""
    # P1 play_corpus_name
    corpus = fields.Str()
    # P2 play_id
    id = fields.Str()
    # P3 play_name (duplicates "name" and "playName")
    name = fields.Str()
    # P4 play_wikidata_id
    wikidataId = fields.Str(allow_none=True)
    # P5 play_title
    title = fields.Str()
    # P7 play_title_en
    titleEn = fields.Str(required=False)
    # P6 play_subtitle
    subtitle = fields.Str(allow_none=True)
    # P8 play_subtitle_en
    subtitleEn = fields.Str(required=False)
    # (deprecated) first author
    author = fields.Nested(FirstAuthorInPlayMetadataSchema)
    # authors as list/array
    authors = fields.List(fields.Nested(AuthorInPlayMetadataSchema))
    # P22 play_genre_normalized
    genre = fields.Str(allow_none=True)
    # P23 play_is_libretto
    libretto = fields.Bool()
    # P24 play_year_written
    yearWritten = fields.Str(allow_none=True)
    # P25 play_year_printed
    yearPrinted = fields.Str(allow_none=True)
    # P26 play_year_premiered
    yearPremiered = fields.Str(allow_none=True)
    # P27 play_year_normalized
    yearNormalized = fields.Int(allow_none=True)
    # P30 play_original_source_full_citation
    originalSource = fields.Str()
    # digital source data
    source = fields.Nested(SourceInPlayMetadataSchema)
    # P50 play_all_in_segment
    # not available in FreDraCor for all plays
    allInSegment = fields.Int(allow_none=True)
    # P51 play_all_in_index [MUST between 0 and 1]
    # not available in FreDraCor for all plays
    allInIndex = fields.Float(validate=validate.Range(0, 1, min_inclusive=True, max_inclusive=True), allow_none=True)
    # P44 play_characters
    cast = fields.List(fields.Nested(CastItemInPlayMetadataSchema))
    # P36 play_segments
    segments = fields.List(fields.Nested(SegmentItemInPlayMetadataSchema))
    # P52 play_character_relations
    relations = fields.List(fields.Nested(RelationItemInPlayMetadataSchema))

# characterGender = fields.Str(validate=validate.OneOf(["male", "female", "nonbinary"]))

