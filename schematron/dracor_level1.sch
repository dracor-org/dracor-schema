<?xml version="1.0" encoding="UTF-8"?>
<schema xmlns="http://purl.oclc.org/dsdl/schematron" queryBinding="xslt2"
    xmlns:sch="http://purl.oclc.org/dsdl/schematron"
    xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
    <ns uri="http://www.tei-c.org/ns/1.0" prefix="tei"/>
    <pattern>
        
        <rule context="tei:TEI">
            <assert test="@xml:lang" role="warning">Attribut "xml:lang" is expected</assert>
            <assert test="matches(@xml:lang,'[a-z]{3}')">Value of attribut "xml:lang" should follow the pattern '[a-z]{3}'</assert>
        </rule>
        
        
        
        <rule context="tei:profileDesc">
            <assert test="tei:particDesc">Element "particDesc" is required</assert>
        </rule>
        
        
    </pattern>
</schema>


