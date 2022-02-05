<?xml version="1.0" encoding="UTF-8"?>
<schema
  xmlns="http://purl.oclc.org/dsdl/schematron"
  xmlns:sch="http://purl.oclc.org/dsdl/schematron"
  xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
  xmlns:tei="http://www.tei-c.org/ns/1.0"
  queryBinding="xslt2"
>
  <ns uri="http://www.tei-c.org/ns/1.0" prefix="tei"/>

  <!--
    Feature: Typical structures of a drama should check:
    - SHOULD contain <sp>
    - SHOULD contain <div> (at least some kind of structure like 'act', 'scene')

    exception; special case:
    - IF NOT <sp> MUST contain at least one <stage> (e.g. "Pantomime")
  -->
  <pattern id="drama-struct">
    <!-- check, if the drama meets basic requirement, should pass all tests -->

    <!--
      MUST have a text/body structure, otherwhise there is not full-text and we
      can't extract anything full-text related
    -->
    <rule id="drama-struct-1" context="tei:TEI">
      <assert id="drama-struct-1-1" test=".//tei:text" role="fatal">
        A drama MUST have a text.
      </assert>
      <assert id="drama-struct-1-2" test=".//tei:text/tei:body" role="fatal">
        A drama MUST have a text body.
      </assert>
    </rule>

    <!--
      SHOULD have typical drama structure, e.g. SHOULD be structured in
      speech-acts
    -->
    <rule id="drama-struct-2" context="tei:body">
      <assert id="drama-struct-2-1" test=".//tei:sp" role="warning">
        A drama SHOULD be structured in speech-acts.
      </assert>
    </rule>

    <!-- COULD be structured in acts -->

    <!-- COULD be structured in scenes -->

    <!-- SHOULD have at least a single structural element <div> -->
    <rule id="drama-struct-3" context="tei:body">
      <assert id="drama-struct-3-1" test="tei:div" role="warning">
        A drama SHOULD at least have one structural division
      </assert>
    </rule>

    <!-- CHECK nesting of acts and scenes -->
    <rule id="drama-struct-4" context="tei:div[@type eq 'scene']">
      <report
        id="drama-struct-4-1"
        role="fatal"
        test=".//tei:div[@type eq 'act']"
      >
        MUST NOT nest acts in scenes
      </report>
    </rule>

    <!--
      Special case: "Pantomime": if there is no speech-act, we expect a
      stage-direction
    -->
    <rule id="drama-struct-5" context="tei:body">
      <assert
        id="drama-struct-5-1"
        role="fatal"
        test="not(.//tei:sp) and .//tei:stage"
      >
        A drama that does not contain a speech-act, MUST at least contain a
        stage direction
      </assert>
    </rule>

  </pattern>

  <!-- Linking speech acts with characters -->

  <pattern id="speaker-ident">
    <let name="allIDs" value="//tei:particDesc//(tei:person|tei:personGrp)/@xml:id/string()"/>
    <!-- particDesc -->
    <!--
      in DraCor context: a drama MUST have a particDesc with a list of
      characters; otherwhise the generation of network metrics will fail
    -->
    <rule id="speaker-ident-1" context="tei:TEI">
      <assert id="speaker-ident-1-1" test=".//tei:particDesc" role="fatal">
        A drama MUST have a "particDesc"
      </assert>
    </rule>

    <!-- particDesc must be nested in profileDesc -->
    <rule id="speaker-ident-2" context="tei:profileDesc">
      <assert id="speaker-ident-2-1" test="tei:particDesc" role="fatal">
        A drama MUST have element "particDesc" in "profileDesc"
      </assert>
    </rule>

    <!-- expect a listPerson in particDesc -->
    <rule id="speaker-ident-3" context="tei:particDesc">
      <assert id="speaker-ident-3-1" test="tei:listPerson" role="fatal">
        A drama MUST have a list of characters as "listPerson"
      </assert>
    </rule>

    <!-- SHOULD be at least one character or group -->
    <rule
      id="speaker-ident-4"
      context="tei:listPerson[ancestor::tei:particDesc]"
    >
      <assert
        id="speaker-ident-4-1"
        test="tei:person or tei:personGrp"
        role="warning"
      >
        There SHOULD be at least on character or group of charaters present.
        Element/s "person" and/or "listPerson" is missing
      </assert>
    </rule>

    <!-- A charater in particDesc -->
    <rule
      id="speaker-ident-5"
      context="tei:person[ancestor::tei:listPerson[ancestor::tei:particDesc]]"
    >
      <let name="localID" value="@xml:id"/>
      <!-- check for xml:ids on person -->
      <assert id="speaker-ident-5-1" test="@xml:id" role="fatal">
        A person MUST have an ID. Attribute "xml:id" is missing
      </assert>

      <!-- should check, if ID is unique! tei-all will do this for xml:id -->

      <!--
        check, if there is a sp or a stage that is actually referencing this ID
      -->
      <assert
        id="speaker-ident-5-2"
        role="warning"
        test="ancestor::tei:TEI//tei:body//tei:sp[@who eq concat('#',$localID)] or ancestor::tei:TEI//tei:body//tei:stage[@who eq concat('#',$localID)]"
      >
        There is no speech act or stage direction, that references the ID of
        this character
      </assert>
    </rule>

    <rule
      id="speaker-ident-6"
      context="tei:personGrp[ancestor::tei:listPerson[ancestor::tei:particDesc]]"
    >
      <let name="localID" value="@xml:id"/>
      <!-- check for xml:id on personGrp -->
      <assert id="speaker-ident-6-1" test="@xml:id" role="fatal">
        A "personGrp" MUST have an ID. Attribute "xml:id" is missing
      </assert>
      <assert
        id="speaker-ident-6-2"
        role="warning"
        test="ancestor::tei:TEI//tei:body//tei:sp[@who eq concat('#',$localID)] or ancestor::tei:TEI//tei:body//tei:stage[@who eq concat('#',$localID)]"
      >
        There is no speech act or stage direction, that references the ID of
        this character
      </assert>
    </rule>

    <!-- all speech-acts SHOULD be linked to chartacters -->
    <rule id="speaker-ident-7" context="tei:TEI">
      <assert
        id="speaker-ident-7-1"
        role="warning"
        test=".//tei:body//tei:sp[@who]"
      >
        There are unlinked speech-acts. Not all elements "sp" have an attribute
        "who"
      </assert>
    </rule>

    <!-- @who -->
    <rule id="speaker-ident-8" context="tei:sp[not(contains(@who,' '))]">
      <let name="localID" value="replace(@who/string(),'#','')"/>
      <assert id="speaker-ident-8-1" test="@who" role="warning">
        A speech act SHOULD be linked to a speaker. Attribute "who" is missing.
      </assert>
      <!-- the id used in who, should exist in the particDesc -->
      <assert
        id="speaker-ident-8-2"
        role="warning"
        test="ancestor::tei:TEI//tei:particDesc//(tei:person|tei:personGrp)[@xml:id eq $localID]"
      >
        Reference SHOULD link to a "person" or "personGrp" in "particDesc"
      </assert>
    </rule>

    <rule id="speaker-ident-9" context="tei:sp[contains(@who,' ')]">
      <let name="localIDs" value="tokenize(@who/string(),'\s+')"/>
      <assert
        id="speaker-ident-9-1"
        role="warning"
        test="every $i in $localIDs satisfies replace($i,'#','') = $allIDs"
      >
        Reference SHOULD link to a "person" or "personGrp" in "particDesc":
        <value-of select="@who/string()"/>
      </assert>
    </rule>
  </pattern>

  <!-- Information on characters -->

  <!-- <assert test="tei:persName">Element "persName" is missing</assert> -->

  <!-- Character Gender information -->
  <pattern id="gender">
    <!-- Hint, that there is no info on gender -->
    <rule
      id="gender-1"
      context="tei:person[ancestor::tei:listPerson[ancestor::tei:particDesc]]"
    >
      <assert id="gender-1-1" test="@sex" role="information">
        Information on gender of character is missing. Consider adding attribute
        "sex"
      </assert>
    </rule>
  </pattern>

  <pattern id="document-language">
    <!-- TEI SHOULD have a xml:lang Attribute -->
    <rule context="tei:TEI" id="document-language-1">
      <assert id="document-language-1-1" test="@xml:lang" role="warning">
        Attribute "xml:lang" is expected
      </assert>
      <assert id="document-language-1-2" test="matches(@xml:lang,'[a-z]{3}')" role="warning">
        Value of attribute "xml:lang" should follow the pattern '[a-z]{3}'
      </assert>
      <!-- 2do check, if it's ISO 639 conformant -->
      <!-- https://de.wikipedia.org/wiki/Listen_der_ISO-639-3-Codes -->
    </rule>
  </pattern>

  <!-- teiHeader Information -->

  <!-- External reference resources -->
  <pattern id="external-references">
    <!-- SHOULD be linked to Wikidata, if possible -->
    <rule id="external-reference-resources-1" context="tei:publicationStmt">
      <assert
        id="external-reference-resources-1-1"
        role="warning"
        test="tei:idno[@type = 'wikidata']"
      >
        Drama is not linked to Wikidata. SHOULD have an element "idno" with
        attribute "type" and alue "wikidata".
      </assert>
    </rule>

    <!--
      Link drama to Wikidata: it should follow a convention: put only the Q
      number there; maybe there is an error in notation of the base-uri IB:
      I think it must be http:// not https:// otherwhise LOD will break
    -->
    <rule id="external-reference-resources-2" context="tei:idno[@type='wikidata']">
      <assert
        id="external-reference-resources-2-1"
        role="warning"
        test="matches(@xml:base,'http://www.wikidata.org/entity/')"
      >
        Check, if value of "xml:base" is aligned with Wikidata namespaces
      </assert>
      <assert
        id="external-reference-resources-2-2"
        role="warning"
        test="matches(text(),'^Q[0-9]+$')"
      >
        Check, if value is a Wikidata-Q-number. Value doesn't match pattern
        '^Q[0-9]+$'
      </assert>
    </rule>
  </pattern>

  <!-- Stuff that needs to be reworked -->
  <pattern>
    <!-- Title of a play -->
    <!--
      A play should at least have one title; if there are more titles, xml:lang
      attributes should be in place; and/or titles should be typed (main/sub)
    -->
    <rule context="tei:titleStmt">
      <assert test="tei:title">
        A play should have a title. Element "title" is missing
      </assert>
    </rule>

    <!-- Author of a play -->

    <!--
      If a play has an author, there should be a link to an external authority
      file
    -->
    <!--
      would have to check, if the correct external authority file is referenced,
      e.g. GND for gerdracor, other should have wikidata
      <rule context="tei:author[parent::tei:titleStmt]">
      </rule>
    -->

    <!-- Licence -->
    <!-- A Licence is required; it should be CC0 if possible -->
    <rule context="tei:availability[ancestor::tei:publicationStmt]">
      <assert test="tei:licence">
        Information on the licence are required. Element "licence" is missing
      </assert>
    </rule>

    <rule context="tei:licence[ancestor::tei:availability[ancestor::tei:publicationStmt]]">
      <assert test="tei:ref">
        A reference to a licence is required. Element "ref" is missing
      </assert>
    </rule>

    <rule context="tei:ref[ancestor::tei:licence[ancestor::tei:availability[ancestor::tei:publicationStmt]]]">
      <assert test="@target">Attribute "target" is missing</assert>
      <assert
        role="information"
        test="contains(@target, 'https://creativecommons.org/publicdomain/zero/1.0')"
      >
        If possible, licence should be CC0
      </assert>
    </rule>
  </pattern>
</schema>
