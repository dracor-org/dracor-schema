<?xml version="1.0" encoding="UTF-8"?>
<!--
  Convert @ana Wikidata URIs on person/personGrp to <idno type="wikidata">
  https://github.com/dracor-org/dracor-schema/issues/130
-->
<xsl:stylesheet
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:tei="http://www.tei-c.org/ns/1.0"
  xmlns:xs="http://www.w3.org/2001/XMLSchema"
  xmlns="http://www.tei-c.org/ns/1.0"
  exclude-result-prefixes="tei xs"
  version="3.0">

  <xsl:output method="xml" />

  <xsl:template
    match="tei:particDesc//(tei:person|tei:personGrp)[@ana[matches(., 'wikidata\.org/(entity|wiki)/Q\d+$')]]">
    <xsl:variable name="last-ws" as="text()?"
      select="text()[last()][normalize-space() = '']"/>
    <xsl:variable name="first-ws" as="text()?"
      select="text()[1][normalize-space() = '']"/>
    <xsl:variable name="parent-indent" as="xs:string"
      select="if ($last-ws) then tokenize($last-ws, '\n')[last()] else ''"/>
    <xsl:variable name="child-indent" as="xs:string"
      select="
        if ($first-ws)
        then tokenize($first-ws, '\n')[last()]
        else concat($parent-indent, '  ')"/>
    <xsl:copy copy-namespaces="no">
      <xsl:apply-templates select="@* except @ana"/>
      <xsl:apply-templates select="node() except $last-ws"/>
      <xsl:text>&#10;</xsl:text>
      <xsl:value-of select="$child-indent"/>
      <idno type="wikidata">
        <xsl:value-of select="tokenize(@ana, '/')[last()]"/>
      </idno>
      <xsl:if test="$last-ws">
        <xsl:value-of select="$last-ws"/>
      </xsl:if>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="@*|*|processing-instruction()|comment()|node()">
    <xsl:copy copy-namespaces="no">
      <xsl:apply-templates select="@*|*|processing-instruction()|comment()|node()"/>
    </xsl:copy>
  </xsl:template>
</xsl:stylesheet>
