<?xml version="1.0" encoding="UTF-8"?>
<!--
  Transform teiCorpus or dracorCorpus to teiHeader as root of corpus.xml
  https://github.com/dracor-org/dracor-schema/issues/108
  https://github.com/dracor-org/dracor-schema/issues/212
-->
<xsl:stylesheet
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:tei="http://www.tei-c.org/ns/1.0"
  xmlns:xi="http://www.w3.org/2001/XInclude"
  xmlns="http://www.tei-c.org/ns/1.0"
  exclude-result-prefixes="tei xi"
  version="3.0">

  <xsl:output method="xml" />

  <xsl:template match="tei:teiCorpus|tei:dracorCorpus">
    <xsl:for-each select="comment()[following-sibling::tei:teiHeader]">
      <xsl:text>
</xsl:text>
      <xsl:copy/>
    </xsl:for-each>
    <xsl:text>
</xsl:text>
    <xsl:apply-templates select="tei:teiHeader"/>
    <xsl:for-each select="comment()[preceding-sibling::tei:teiHeader]">
      <xsl:text>
</xsl:text>
      <xsl:copy/>
    </xsl:for-each>
    <xsl:text>
</xsl:text>
  </xsl:template>

  <!-- remove one level of indentation from the former teiHeader descendants -->
  <xsl:template match="tei:teiHeader[parent::tei:teiCorpus or parent::tei:dracorCorpus]//text()">
    <xsl:value-of select="replace(., '&#10;  ', '&#10;')"/>
  </xsl:template>

  <xsl:template match="tei:teiHeader[parent::tei:teiCorpus or parent::tei:dracorCorpus]//comment()">
    <xsl:comment select="replace(., '&#10;  ', '&#10;')"/>
  </xsl:template>

  <xsl:template match="tei:publicationStmt[not(/tei:TEI)]">
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

  <xsl:template match="tei:idno[@type='URI' and @xml:base='https://dracor.org/'][not(/tei:TEI)]">
    <idno>
      <xsl:value-of select="text()"/>
    </idno>
  </xsl:template>

  <xsl:template match="tei:idno[@type='repo'][not(/tei:TEI)]">
    <ref type="repo" target="{text()}"/>
  </xsl:template>

  <xsl:template match="@*|*|processing-instruction()|comment()|node()">
    <xsl:copy copy-namespaces="no">
      <xsl:apply-templates select="@*|*|processing-instruction()|comment()|node()"/>
    </xsl:copy>
  </xsl:template>
</xsl:stylesheet>
