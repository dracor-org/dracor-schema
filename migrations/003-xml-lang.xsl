<?xml version="1.0" encoding="UTF-8"?>
<!--
  Replace 3-letter ISO-639 codes with 2-letter ones.
  https://github.com/dracor-org/dracor-schema/issues/123
-->
<xsl:stylesheet
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:tei="http://www.tei-c.org/ns/1.0"
  xmlns:map="http://www.w3.org/2005/xpath-functions/map"
  xmlns="http://www.tei-c.org/ns/1.0"
  exclude-result-prefixes="tei"
  version="3.0">

  <xsl:output method="xml" encoding="utf-8"/>

  <!--
    Mapping 3-letter codes found in DraCor corpora to 2-letter or more
    appropriate 3-letter ones.

    Note: In EngDraCor there is currently the non-standard code 'unk' used
    multiple times for apparently badly OCRed sequences of characters. We leave
    it untouched, as we do with the standard 'mis' used for gibberish text.
  -->
  <xsl:variable name="codes" select="map {
    'bak': 'ba',
    'cze': 'cz',
    'dut': 'nl',
    'ell': 'grc',
    'eng': 'en',
    'fra': 'fr',
    'fre': 'fr',
    'fro': 'fr',
    'geo': 'ka',
    'ger': 'de',
    'gre': 'grc',
    'gsw': 'gsw',
    'heb': 'he',
    'hun': 'hu',
    'ita': 'it',
    'lat': 'la',
    'mis': 'mis',
    'nob': 'no',
    'pol': 'pl',
    'rom': 'ro',
    'rus': 'ru',
    'spa': 'es',
    'tat': 'tt',
    'tmr': 'tmr',
    'ukr': 'uk',
    'yid': 'yid'
  }"/>

  <xsl:variable name="iso3" select="map:keys($codes)"/>

  <xsl:template match="@xml:lang[. = $iso3]">
    <xsl:variable name="val" select="string(.)"/>
    <xsl:attribute name="xml:lang">
      <xsl:value-of select="$codes($val)"/>
    </xsl:attribute>
  </xsl:template>

  <xsl:template match="@*|*|processing-instruction()|comment()|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|*|processing-instruction()|comment()|node()"/>
    </xsl:copy>
  </xsl:template>
</xsl:stylesheet>
