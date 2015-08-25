<?xml version='1.0' encoding='UTF-8'?>

<!-- 
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 -->

<!-- 
  Simple transform of Solr query results to DataONE ObjectList
  ... &fl=id,size,objectformat,checksum,checksumAlgorithm,datemodified&wt=xslt&tr=d1olist.xsl
 -->
<xsl:stylesheet version='1.0'
    xmlns:xsl='http://www.w3.org/1999/XSL/Transform'
>

  <xsl:output
       method="xml"
       encoding="UTF-8"
       media-type="application/xml"
       indent="yes"
  />
  
  <xsl:variable name="nfound" select="response/result/@numFound"/>
  <xsl:variable name="start" select="response/result/@start"/>
  <xsl:variable name="nrecs" select="count(response/result/doc)" />
  
  <xsl:template match='/'>
    <d1:log xmlns:d1="http://ns.dataone.org/service/types/v1" count="{$nrecs}" start="{$start}" total="{$nfound}"> 
        <xsl:apply-templates select="response/result/doc"/>
    </d1:log>
  </xsl:template>
  
  <xsl:template match="doc">
    <logEntry>
      <entryId><xsl:value-of select="str[@name='entryId']"/></entryId>
      <identifier><xsl:value-of select="str[@name='pid']"/></identifier>
      <ipAddress><xsl:value-of select="str[@name='ipAddress']"/></ipAddress>
      <userAgent><xsl:value-of select="str[@name='userAgent']"/></userAgent>
      <subject><xsl:value-of select="str[@name='subject']"/></subject>
      <event><xsl:value-of select="str[@name='event']"/></event>
      <dateLogged><xsl:value-of select="date[@name='dateLogged']"/></dateLogged>
      <nodeIdentifier><xsl:value-of select="str[@name='nodeId']"/></nodeIdentifier>
    </logEntry>
  </xsl:template>
</xsl:stylesheet>
