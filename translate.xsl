<xsl:stylesheet version="2.0"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:shipping="http://www.w3.org/1999/XSL/Transform"
	exclude-result-prefixes="shipping"
	>
	<!-- 
		SHIPPING FORECAST READER 
		Converts the UK Shipping forecast into readable 
		format. 
		
		Uses as source the Met Office XML feed of the Shipping forecast 
		https://www.metoffice.gov.uk/public/data/CoreProductCache/ShippingForecast/Latest -->
	
   	<xsl:function name="shipping:timeFormat">
   		<xsl:param name="time"/>
   		<xsl:value-of select="substring($time,1,1)"/>-
   		<xsl:value-of select="substring($time,2,1)"/>-
   		<xsl:value-of select="substring($time,3,1)"/>-
   		<xsl:value-of select="substring($time,4,1)"/>
  	</xsl:function>
  	
	<xsl:template match="/report">
		And now the Shipping Forecast, issued by the Met Office on behalf of the Maritime and Coastguard Agency at <xsl:value-of select="issue/@time"></xsl:value-of> today.
		
		<xsl:if test="count(gales) &gt; 0">
			<xsl:if test="count(gales/shipping-area) &gt; 0">
				<xsl:if test="count(gales/shipping-area) = 1"> 
					There is a gale warning for <xsl:value-of select="gales/shipping-area[1]"></xsl:value-of>.
				</xsl:if>
				<xsl:if test="count(gales/shipping-area) &gt; 1">
					There are gale warnings for 
					<xsl:for-each select="gales/shipping-area[position() &lt; last() - 1]">
						<xsl:value-of select="."></xsl:value-of>, 
					</xsl:for-each>
					<xsl:value-of select="gales/shipping-area[last() - 1 ]"></xsl:value-of> 
					and 
					<xsl:value-of select="gales/shipping-area[last()]"></xsl:value-of>.
				</xsl:if>
			</xsl:if>
		</xsl:if>
		
		The General Synopsis at <xsl:value-of select="general-synopsis/valid/@time"></xsl:value-of>:
		<xsl:value-of select="general-synopsis/gs-text"></xsl:value-of>.
		
		The Area Forecasts for the next <xsl:value-of select="area-forecasts/@period"></xsl:value-of> hours:
		
		<xsl:for-each select="area-forecasts/area-forecast">
			<xsl:value-of select="all"></xsl:value-of>: 
			<xsl:value-of select="wind"></xsl:value-of>.
			<xsl:value-of select="weather"></xsl:value-of>.
			<xsl:value-of select="visibility"></xsl:value-of>.
		</xsl:for-each>
		
		And that's the Shipping Forecast.
	</xsl:template>
</xsl:stylesheet>