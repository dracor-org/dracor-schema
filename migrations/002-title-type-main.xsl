<?xml version="1.0" encoding="UTF-8"?>
<!--
  Remove type="main" from main title in the teiHeader
  https://github.com/dracor-org/dracor-schema/issues/152
-->
<xsl:stylesheet
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:tei="http://www.tei-c.org/ns/1.0"
  xmlns="http://www.tei-c.org/ns/1.0"
  exclude-result-prefixes="tei"
  version="3.0">

  <xsl:output method="xml" encoding="utf-8"/>

  <xsl:template match="tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title[@type = 'main']/@type">
  </xsl:template>

  <xsl:template match="@*|*|processing-instruction()|comment()|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|*|processing-instruction()|comment()|node()"/>
    </xsl:copy>
  </xsl:template>
</xsl:stylesheet>
