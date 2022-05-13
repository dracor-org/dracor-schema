<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:tei="http://www.tei-c.org/ns/1.0"
  xmlns="http://www.tei-c.org/ns/1.0"
  exclude-result-prefixes="tei"
  version="3.0">

  <xsl:output method="xml" encoding="utf-8" omit-xml-declaration="no" indent="yes"/>

  <xsl:template match="@*|*|processing-instruction()|comment()|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|*|processing-instruction()|comment()|node()"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="tei:teiHeader">
    <xsl:variable name="dates" select="/tei:TEI/tei:teiHeader//tei:sourceDesc//tei:bibl[@type='originalSource']/tei:date[@type='print' or  @type='premiere' or @type='written'][@when != '' or @notBefore or @notAfter]"/>
    <xsl:variable name="wd-idno" select="/tei:TEI//tei:publicationStmt/tei:idno[@type='wikidata']"/>
    <teiHeader>
      <xsl:apply-templates/>
    </teiHeader>
    <standOff>
      <xsl:if test="$dates">
        <listEvent>
          <xsl:for-each select="$dates">
            <event type="{@type}">
              <xsl:for-each select="@when|@notBefore|@notAfter">
                <xsl:attribute name="{local-name()}">
                  <xsl:value-of select="."/>
                </xsl:attribute>
              </xsl:for-each>
              <desc>
                <xsl:value-of select="./text()"/>
              </desc>
            </event>
          </xsl:for-each>
        </listEvent>
      </xsl:if>
      <xsl:if test="$wd-idno">
        <link type="wikidata" target="Q51529377">
          <xsl:attribute name="target">
            <xsl:text>http://www.wikidata.org/entity/</xsl:text>
            <xsl:value-of select="$wd-idno/text()"/>
          </xsl:attribute>
        </link>
      </xsl:if>
    </standOff>
  </xsl:template>

  <!-- strip old elements  -->
  <xsl:template match="tei:sourceDesc//tei:bibl[@type='originalSource']/tei:date[@type='print' or  @type='premiere' or @type='written']" />
  <xsl:template match="tei:publicationStmt/tei:idno[@type='wikidata']" />
</xsl:stylesheet>
