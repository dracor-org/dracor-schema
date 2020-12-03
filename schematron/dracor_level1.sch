<?xml version="1.0" encoding="UTF-8"?>
<schema xmlns="http://purl.oclc.org/dsdl/schematron" queryBinding="xslt2"
    xmlns:sch="http://purl.oclc.org/dsdl/schematron"
    xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
    <ns uri="http://www.tei-c.org/ns/1.0" prefix="tei"/>
    <pattern>
        
        <rule context="tei:TEI">
            <assert test="@xml:lang" role="warning">Attribut "xml:lang" is expected</assert>
            <assert test="matches(@xml:lang,'[a-z]{3}')" role="warning">Value of attribut "xml:lang" should follow the pattern '[a-z]{3}'</assert>
            <!-- 2do check, if it's ISO X conformant -->
        </rule>
        
        <rule context="tei:titleStmt">
            <assert test="tei:title">A play should have a title. Element "title" is missing</assert>
        </rule>
        
        
        <rule context="tei:author[parent::tei:titleStmt]">
            <assert test="@key" role="warning">The author of a play should be linked to an external authority file. Attribute "key" is missing</assert>
            <!-- would have to check, if the correct external authority file is referenced, e.g. GND for gerdracor, other should have wikidata -->
        </rule>
        
        <rule context="tei:publicationStmt">
            <assert test="tei:idno[@type = 'wikidata']" role="warning">Play is not linked to Wikidata. Element "idno" is missing</assert>
        </rule>
        
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
        
        <rule context="tei:profileDesc">
            <assert test="tei:particDesc">Element "particDesc" is required</assert>
        </rule>
        
        
    </pattern>
</schema>


