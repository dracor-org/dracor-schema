<?xml version="1.0" encoding="UTF-8"?>
<!--
  Simplify markup of licence information
  https://github.com/dracor-org/dracor-schema/issues/97
-->
<xsl:stylesheet
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:tei="http://www.tei-c.org/ns/1.0"
  xmlns="http://www.tei-c.org/ns/1.0"
  exclude-result-prefixes="tei"
  version="3.0">

  <!-- <xsl:output method="xml" encoding="utf-8" omit-xml-declaration="no" indent="no"/> -->
  <xsl:output method="xml" encoding="utf-8"/>

  <xsl:template match="tei:licence[count(tei:ab) eq 1 and count(tei:ref[@target]) eq 1]">
    <xsl:variable name="title" select="normalize-space(tei:ab)"/>
    <xsl:variable name="target" select="tei:ref/@target/string()"/>
    <licence>
      <xsl:attribute name="target" select="$target"/>
      <xsl:value-of select="$title"/>
    </licence>
  </xsl:template>

  <xsl:template match="@*|*|processing-instruction()|comment()|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|*|processing-instruction()|comment()|node()"/>
    </xsl:copy>
  </xsl:template>
</xsl:stylesheet>
