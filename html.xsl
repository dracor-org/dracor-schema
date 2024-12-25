<?xml version="1.0" encoding="UTF-8"?>
<!--
This stylesheet post-processes the HTML rendering of the ODD as generated by the
TEI Stylesheets.
-->
<xsl:stylesheet
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:tei="http://www.tei-c.org/ns/1.0"
  xmlns:h="http://www.w3.org/1999/xhtml"
  xmlns="http://www.w3.org/1999/xhtml"
  exclude-result-prefixes="tei h"
  version="3.0">

  <xsl:output method="xml" encoding="utf-8" omit-xml-declaration="yes" indent="no"/>

  <xsl:param name="version"/>

  <xsl:variable name="ids" select="//h:ul[@id='dracor-tei-elements']/h:li/h:a/@href/substring-after(., '#')"/>

  <xsl:template match="@*|*|processing-instruction()|comment()|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|*|processing-instruction()|comment()|node()"/>
    </xsl:copy>
  </xsl:template>

  <!-- add class "non-dracor" to non-DraCor elements and switch to non-Dracor mode -->
  <xsl:template match="h:div[h:h2[ends-with(normalize-space(.), 'Elements')]]/h:div[@class='refdoc' and starts-with(@id, 'TEI.') and not(@id = $ids)]">
    <div class="refdoc non-dracor" id="{@id}">
      <xsl:apply-templates select="*" mode="non-dracor"/>
    </div>
  </xsl:template>

  <!-- catch-all template for non-nracor mode -->
  <xsl:template match="*|@*" mode="non-dracor">
    <xsl:copy>
      <xsl:apply-templates select="@*|*|comment()|node()" mode="non-dracor"/>
    </xsl:copy>
  </xsl:template>

  <!-- insert version -->
  <xsl:template match="h:div[@class = 'titlePage']">
    <xsl:copy>
      <xsl:apply-templates select="@*|*"/>
      <xsl:if test="$version">
        <div class="dracor-schema-version">
          <small>
            <xsl:value-of select="$version"/>
          </small>
        </div>
      </xsl:if>
    </xsl:copy>
  </xsl:template>

  <!-- add note and link to TEI documentation for non-DraCor elements -->
  <xsl:template match="h:h3" mode="non-dracor">
    <xsl:variable name="ref" select="substring-after(parent::h:div[@class = 'refdoc']/@id, 'TEI.')"/>
    <xsl:copy>
      <xsl:apply-templates select="@*|*" mode="non-dracor"/>
    </xsl:copy>
    <p>
      <em>This element is currently not <a href="#section-list-used-elems">actively
      used</a> in DraCor. See <a href="https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-{$ref}.html" target="tei-guidelines">full
      documentation in TEI Guidelines</a>.</em>
    </p>
  </xsl:template>

  <!-- remove non-DraCor examples  -->
  <xsl:template match="h:tr[normalize-space(./h:td[1]) = 'Example']" mode="non-dracor">
    <xsl:comment>removed example</xsl:comment>
  </xsl:template>
</xsl:stylesheet>
