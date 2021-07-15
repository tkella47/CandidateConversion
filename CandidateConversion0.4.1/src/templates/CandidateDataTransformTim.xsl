<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
 <xsl:output method="text" encoding="UTF-8"/> 
 
  <xsl:template match="/">
  <xsl:text>CandidateID|FileName</xsl:text>
  <xsl:text>&#xD;&#xA;</xsl:text> 
    <xsl:apply-templates select="/files/file"/>
    
  </xsl:template>
  
   <xsl:template match="/files/file">
 		<xsl:value-of select="CandidateID"/>
   <xsl:value-of select="FileName"/>
		<xsl:text>&#xa;</xsl:text>	
   </xsl:template>
</xsl:stylesheet>
