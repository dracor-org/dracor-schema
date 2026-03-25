<?xml version="1.0" encoding="UTF-8"?>
<!--
  Transform teiCorpus to dracorCorpus
  https://github.com/dracor-org/dracor-schema/issues/108
-->
<xsl:stylesheet
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:tei="http://www.tei-c.org/ns/1.0"
  xmlns:xi="http://www.w3.org/2001/XInclude"
  xmlns="http://www.tei-c.org/ns/1.0"
  exclude-result-prefixes="tei xi"
  version="3.0">

  <xsl:output method="xml" />

  <xsl:template match="tei:teiCorpus">
    <xsl:text>
</xsl:text>
    <dracorCorpus>
      <xsl:apply-templates select="*|node()|comment()"/>
    </dracorCorpus>
    <xsl:text>
</xsl:text>
  </xsl:template>

  <xsl:template match="tei:publicationStmt">
    <xsl:copy copy-namespaces="no">
      <xsl:apply-templates select="@*|*|node()|comment()"/>
    </xsl:copy>
    <xsl:if test="not(./following-sibling::tei:sourceDesc)">
      <xsl:text>
      </xsl:text>
      <sourceDesc>
        <xsl:text>
        </xsl:text>
        <p>See source information in individual TEI files.</p>
        <xsl:text>
      </xsl:text>
      </sourceDesc>
    </xsl:if>
  </xsl:template>

  <xsl:template match="tei:idno[@type='URI' and @xml:base='https://dracor.org/']">
    <idno>
      <xsl:value-of select="text()"/>
    </idno>
  </xsl:template>

  <xsl:template match="tei:idno[@type='repo']">
    <ref type="repo" target="{text()}"/>
  </xsl:template>

  <xsl:template match="@*|*|processing-instruction()|comment()|node()">
    <xsl:copy copy-namespaces="no">
      <xsl:apply-templates select="@*|*|processing-instruction()|comment()|node()"/>
    </xsl:copy>
  </xsl:template>
</xsl:stylesheet>
