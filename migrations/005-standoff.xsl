<?xml version="1.0" encoding="UTF-8"?>
<!--
  Retire standOff
  https://github.com/dracor-org/dracor-schema/issues/133
-->
<xsl:stylesheet
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:tei="http://www.tei-c.org/ns/1.0"
  xmlns="http://www.tei-c.org/ns/1.0"
  exclude-result-prefixes="tei"
  version="3.0">

  <xsl:output method="xml" />

  <xsl:template match="tei:sourceDesc[not(tei:bibl[@type='wikidata'])]">
    <xsl:variable
      name="relation"
      select="//tei:standOff/tei:listRelation/tei:relation[
        @name='wikidata' and starts-with(@passive, 'http://www.wikidata.org/entity/Q')
      ]"/>
    <xsl:variable name="events" select="//tei:standOff/tei:listEvent[tei:event[@type = ('print', 'written', 'premiere')]]"/>
    <xsl:copy>
      <xsl:apply-templates />
      <xsl:if test="exists($relation)">
        <bibl type="wikidata">
          <idno>
            <xsl:value-of select="substring-after($relation/@passive, 'http://www.wikidata.org/entity/')"/>
          </idno>
        </bibl>
        <xsl:text>
        </xsl:text>
      </xsl:if>
      <xsl:if test="exists($events)">
        <xsl:copy-of select="$events"/>
      </xsl:if>
      <xsl:text>
      </xsl:text>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="tei:standOff">
  </xsl:template>

  <xsl:template match="@*|*|processing-instruction()|comment()|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|*|processing-instruction()|comment()|node()"/>
    </xsl:copy>
  </xsl:template>
</xsl:stylesheet>
