<?xml version="1.0" encoding="UTF-8"?>
<schema xmlns="http://purl.oclc.org/dsdl/schematron" queryBinding="xslt2"
    xmlns:sch="http://purl.oclc.org/dsdl/schematron"
    xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
    <ns uri="http://www.tei-c.org/ns/1.0" prefix="tei"/>
    <pattern>
        
        <!-- TEI -->
        <!-- TEI should have a xml:lang Attribute -->
        <rule context="tei:TEI">
            <assert test="@xml:lang" role="warning">Attribut "xml:lang" is expected</assert>
            <assert test="matches(@xml:lang,'[a-z]{3}')" role="warning">Value of attribut "xml:lang" should follow the pattern '[a-z]{3}'</assert>
            <!-- 2do check, if it's ISO 639 conformant -->
            <!-- https://de.wikipedia.org/wiki/Listen_der_ISO-639-3-Codes -->
        </rule>
        
        <!-- Title of a play -->
        <!-- A play should at least have one title; if there are more titles, xml:lang Attributes should be in place; and/or titles should be typed (main/sub) -->
        <rule context="tei:titleStmt">
            <assert test="tei:title">A play should have a title. Element "title" is missing</assert>
        </rule>
        
        <!-- Autor of a play -->
        <!-- If a play has an author, there should be a link to an external authority file -->
        <rule context="tei:author[parent::tei:titleStmt]">
            <assert test="@key" role="warning">The author of a play should be linked to an external authority file. Attribute "key" is missing</assert>
            <!-- would have to check, if the correct external authority file is referenced, e.g. GND for gerdracor, other should have wikidata -->
        </rule>
        
        <!-- Plays should be linked to Wikidata, if possible -->
        <rule context="tei:publicationStmt">
            <assert test="tei:idno[@type = 'wikidata']" role="warning">Play is not linked to Wikidata. Element "idno" is missing</assert>
        </rule>
        
        <!-- Licence -->
        <!-- A Licence is required; it should be CC0 if possible -->
        <rule context="tei:availability[ancestor::tei:publicationStmt]">
            <assert test="tei:licence">Information on the licence are required. Element "licence" is missing</assert>
        </rule>
        
        <rule context="tei:licence[ancestor::tei:availability[ancestor::tei:publicationStmt]]">
            <assert test="tei:ref">A reference to a licence is required. Element "ref" is missing</assert>
        </rule>
        
        <rule context="tei:ref[ancestor::tei:licence[ancestor::tei:availability[ancestor::tei:publicationStmt]]]">
            <assert test="@target">Attribute "target" is missing</assert>
            <assert test="contains(@target, 'https://creativecommons.org/publicdomain/zero/1.0')" role="information">If possible, licence should be CC0</assert>
        </rule>
        
        
        <!-- Link Play to Wikidata: it should follow a convention: put only the Q number there; maybe there is an error in notation of the base-uri IB: I think it must be http:// not https:// otherwhise LOD will break -->
        <rule context="tei:idno[@type='wikidata']">
            <assert test="matches(@xml:base,'http://www.wikidata.org/entity/')" role="warning">Check, if value of "xml:base" is aligned with Wikidata-Namespaces</assert>
            <assert test="matches(text(),'^Q[0-9]+$')" role="warning">Check, if value is a Wikidata-Q-Number. Value doesn't match pattern '^Q[0-9]+$'</assert>
        </rule>
        
        <!-- particDesc -->
        <!-- a play must have a particDesc with a list of characters; otherwhise generation of network metrics won't work -->
        <rule context="tei:profileDesc">
            <assert test="tei:particDesc">Element "particDesc" is required</assert>
        </rule>
        
        <rule context="tei:particDesc">
            <assert test="tei:listPerson">A list of characters as "listPerson" is required</assert>
        </rule>
        
        <rule context="tei:listPerson[ancestor::tei:particDesc]">
            <assert test="tei:person or tei:personGrp">There must be at least on character or group of charaters present. Element/s "person" and/or "listPerson" is missing</assert>
        </rule>
        
        <!-- A charater in particDesc -->
        <rule context="tei:person[ancestor::tei:listPerson[ancestor::tei:particDesc]]">
            <assert test="@xml:id">A person must have an ID. Element "xml:id" is missing</assert>
            <!-- should check, if ID is unique! tei-all will do this for xml:id -->
            
            <!-- check, if there is a sp or a stage that is actually referencing this id -->
            <let name="localID" value="@xml:id"/>
            <assert test="ancestor::tei:TEI//tei:body//tei:sp[@who eq concat('#',$localID)] or ancestor::tei:TEI//tei:body//tei:stage[@who eq concat('#',$localID)]" role="information">There is no speech, that references the ID of this character</assert>
            
            <assert test="@sex" role="information">Information on gender of character is missing. Consider adding attribute "sex"</assert>
            
            <assert test="tei:persName">Element "persName" is missing</assert>
        </rule>
        
        <!-- ... -->
        
      
        
        
        
    </pattern>
</schema>


