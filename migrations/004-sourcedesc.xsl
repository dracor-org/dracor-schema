<?xml version="1.0" encoding="UTF-8"?>
<!--
  Dissolve originalSource nested in digitalSource
  https://github.com/dracor-org/dracor-schema/issues/107
-->
<xsl:stylesheet
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:tei="http://www.tei-c.org/ns/1.0"
  xmlns="http://www.tei-c.org/ns/1.0"
  exclude-result-prefixes="tei"
  version="3.0">

  <xsl:output method="xml" encoding="UTF-8"/>

  <xsl:template match="tei:bibl[@type = 'digitalSource' and tei:bibl[@type='originalSource']]">
    <xsl:copy>
      <xsl:apply-templates select="@*|*[not(@type='originalSource')]|node() except tei:bibl[@type='originalSource']"/>
    </xsl:copy>
    <xsl:text>
        </xsl:text>
    <xsl:apply-templates select="tei:bibl[@type='originalSource']"/>
  </xsl:template>

  <xsl:template match="tei:bibl[@type = 'digitalSource']/tei:idno[@type='URL' and preceding-sibling::tei:name]">
    <xsl:variable name="url" select="text()"/>
    <ref>
      <xsl:attribute name="target" select="$url"/>
      <xsl:value-of select="preceding-sibling::tei:name/text()"/>
    </ref>
  </xsl:template>

  <xsl:template match="tei:bibl[@type = 'digitalSource']/tei:name[following-sibling::tei:idno[@type='URL']]">
  </xsl:template>

  <xsl:template match="@*|*|processing-instruction()|comment()|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|*|processing-instruction()|comment()|node()"/>
    </xsl:copy>
  </xsl:template>
</xsl:stylesheet>
