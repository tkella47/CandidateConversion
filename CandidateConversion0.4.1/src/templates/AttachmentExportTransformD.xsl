<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:output method="xml" omit-xml-declaration="yes" encoding="UTF-8" indent="yes"/>
	<xsl:template name="substring-after-last">
	  <xsl:param name="string" />
	  <xsl:param name="delimiter" />
	  <xsl:choose>
		<xsl:when test="contains($string, $delimiter)">
		  <xsl:call-template name="substring-after-last">
			<xsl:with-param name="string"
			  select="substring-after($string, $delimiter)" />
			<xsl:with-param name="delimiter" select="$delimiter" />
		  </xsl:call-template>
		</xsl:when>
		<xsl:otherwise><xsl:value-of select="$string" /></xsl:otherwise>
	  </xsl:choose>
	</xsl:template>
 <!-- <xsl:output method="text" encoding="UTF-8"/> -->
   <xsl:template match="/">
     <xsl:element name="file">	 
	  <xsl:variable name="lastchar" select="*[local-name()='record']/*[local-name()='field'][@name='AttachmentFileName']"/>	
	    <xsl:variable name="FileExt">
		<xsl:call-template name="substring-after-last">
		  <xsl:with-param name="string" select="$lastchar"/>
      <xsl:with-param name="delimiter" select="'.'"/>
     </xsl:call-template>
	  </xsl:variable>
       <xsl:attribute name="path">
	   	    <xsl:value-of select="*[local-name()='record']/*[local-name()='field'][@name='CandidateID']"/>_<xsl:value-of select="*[local-name()='record']/*[local-name()='field'][@name='DocNumber']"/>.<xsl:value-of select="$FileExt"/>
         <!-- <xsl:value-of select="*[local-name()='record']/*[local-name()='field'][@name='CandidateID']"/>_<xsl:value-of select="*[local-name()='record']/*[local-name()='field'][@name='FirstName']"/>_<xsl:value-of select="*[local-name()='record']/*[local-name()='field'][@name='LastName']"/>.<xsl:value-of select="$FileExt"/> -->
       </xsl:attribute>
	   <xsl:element name="CandidateID">
       <xsl:value-of select="*[local-name()='record']/*[local-name()='field'][@name='CandidateID']"/>
       </xsl:element>
	   <xsl:element name="FileName">
	    <xsl:value-of select="*[local-name()='record']/*[local-name()='field'][@name='CandidateID']"/>_<xsl:value-of select="*[local-name()='record']/*[local-name()='field'][@name='DocNumber']"/>.<xsl:value-of select="$FileExt"/>
       <!-- <xsl:value-of select="*[local-name()='record']/*[local-name()='field'][@name='CandidateID']"/>_<xsl:value-of select="*[local-name()='record']/*[local-name()='field'][@name='FirstName']"/>_<xsl:value-of select="*[local-name()='record']/*[local-name()='field'][@name='LastName']"/>.<xsl:value-of select="$FileExt"/> -->
       </xsl:element>
	    <xsl:element name="content">
        <xsl:value-of select="*[local-name()='record']/*[local-name()='field'][@name='AttachmentFileContent']"/>
       </xsl:element>
     </xsl:element>
   </xsl:template>
</xsl:stylesheet>