<?xml version="1.0" encoding="UTF-8"?>
<schema xmlns="http://purl.oclc.org/dsdl/schematron" queryBinding="xslt2"
    xmlns:sch="http://purl.oclc.org/dsdl/schematron"
    xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
    <ns uri="http://www.tei-c.org/ns/1.0" prefix="tei"/>
    <pattern>
        <rule context="tei:profileDesc">
            <assert test="tei:particDesc">Element "particDesc" is required</assert>
        </rule>
        
        
    </pattern>
</schema>


