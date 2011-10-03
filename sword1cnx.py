"""
Library for interacting with Connexions through its SWORD version 1
API.

Author: Carl Scheffler
Copyright (C) 2011 Katherine Fletcher.

Funding was provided by The Shuttleworth Foundation as part of the OER
Roadmap Project.

If the license this software is distributed under is not suitable for
your purposes, you may contact the copyright holder through
oer-roadmap-discuss@googlegroups.com to discuss different licensing
terms.

This file is part of oerpub.rhaptoslabs.sword1cnx

Sword1Cnx is free software: you can redistribute it and/or modify it
under the terms of the GNU Lesser General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Sword1Cnx is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with Sword1Cnx.  If not, see <http://www.gnu.org/licenses/>.
"""
from __future__ import division
from sword1 import *

def parse_service_document(serviceDoc):
    """
    Read available collections from the service document.
    """
    serviceDocLower = serviceDoc.lower()
    pos = 0
    swordCollections = []
    while True:
        # Get url
        subString = '<collection href="'
        pos0 = serviceDocLower.find(subString, pos)
        if pos0 == -1:
            break
        pos0 += len(subString)
        pos1 = serviceDocLower.find('">', pos0)
        url = serviceDoc[pos0:pos1]
        pos = pos1
        # Get collection entity extent
        posCollectionEnd = serviceDocLower.find('</collection>', pos)
        # Get title
        subString = '<atom:title>'
        pos0 = serviceDocLower.find(subString, pos)
        if (pos0 == -1) or (pos0 > posCollectionEnd):
            break
        pos0 += len(subString)
        pos1 = serviceDocLower.find('</atom:title>', pos0)
        title = serviceDoc[pos0:pos1]
        pos = pos1
        # Check that it accepts zip files
        pos0 = serviceDocLower.find('<accept>application/zip</accept>', pos)
        if (pos0 == -1) or (pos0 > posCollectionEnd):
            break
        # Store
        swordCollections.append({'url': url, 'title': title})

    return swordCollections

def create_mets(title, summary, language, keywords):
    """
    Return the text content that should go into the mets.xml to encode
    the metadata of a Connexions module.

    Inputs:
      title  Title of the module (string).
      summary  Summary of the module (string).
      language  The two-letter ISO 639-1 language code of the module (string).
      keywords  Keywords describing the module (list of strings).

    Returns: a string containing the METS.
    """

    return """<?xml version="1.0" encoding="utf-8" standalone="no" ?>
<mets ID="sort-mets_mets" OBJID="sword-mets" LABEL="DSpace SWORD Item" PROFILE="DSpace METS SIP Profile 1.0" xmlns="http://www.loc.gov/METS/" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.loc.gov/METS/ http://www.loc.gov/standards/mets/mets.xsd">

  <metsHdr CREATEDATE="2008-09-04T00:00:00">
    <agent ROLE="CUSTODIAN" TYPE="ORGANIZATION">
      <name>Unknown</name>
    </agent>
  </metsHdr>

  <dmdSec ID="sword-mets-dmd-1" GROUPID="sword-mets-dmd-1_group-1">
    <mdWrap LABEL="SWAP Metadata" MDTYPE="OTHER" OTHERMDTYPE="EPDCX" MIMETYPE="text/xml">
      <xmlData>
        <epdcx:descriptionSet xmlns:epdcx="http://purl.org/eprint/epdcx/2006-11-16/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://purl.org/eprint/epdcx/2006-11-16/ http://purl.org/eprint/epdcx/xsd/2006-11-16/epdcx.xsd">
          <epdcx:description epdcx:resourceId="sword-mets-epdcx-1">
            <epdcx:statement epdcx:propertyURI="http://purl.org/dc/elements/1.1/title">
              <epdcx:valueString>""" + title + """</epdcx:valueString>
            </epdcx:statement>
            <epdcx:statement epdcx:propertyURI="http://purl.org/dc/terms/abstract">
              <epdcx:valueString>""" + summary + """</epdcx:valueString>
            </epdcx:statement>
            <epdcx:statement epdcx:propertyURI="http://purl.org/eprint/terms/isExpressedAs" epdcx:valueRef="sword-mets-expr-1" />
          </epdcx:description>
          <epdcx:description epdcx:resourceId="sword-mets-expr-1">
            <epdcx:statement epdcx:propertyURI="http://purl.org/dc/elements/1.1/type" epdcx:valueURI="http://purl.org/eprint/entityType/Expression" />
            <epdcx:statement epdcx:propertyURI="http://purl.org/dc/elements/1.1/type" epdcx:vesURI="http://purl.org/eprint/terms/Type" epdcx:valueURI="http://purl.org/eprint/entityType/Expression" />
          </epdcx:description>
	  <epdcx:description epdcx:resourceId="sword-mets-expr-1">
	    <epdcx:statement epdcx:propertyURI="http://purl.org/dc/elements/1.1/type" epdcx:valueURI="http://purl.org/eprint/entityType/Expression" />
	    <epdcx:statement epdcx:propertyURI="http://purl.org/dc/elements/1.1/language" epdcx:vesURI="http://purl.org/dc/terms/RFC3066">
	      <epdcx:valueString>""" + language + """</epdcx:valueString>
	    </epdcx:statement>
	    <epdcx:statement epdcx:propertyURI="http://purl.org/dc/elements/1.1/type" epdcx:vesURI="http://purl.org/eprint/terms/Type" epdcx:valueURI="http://purl.org/eprint/entityType/Expression" />
	    <epdcx:statement epdcx:propertyURI="http://purl.org/eprint/terms/bibliographicCitation">
	      <epdcx:valueString>
		<bib:file xmlns:bib="http://bibtexml.sf.net/">
		  <bib:entry>
                    """ +  "".join(['<bib:keywords>' + keyword + '</bib:keywords>'
                for keyword in [_.strip() for _ in keywords] if keyword != '']) + """
		  </bib:entry>
		</bib:file>
	      </epdcx:valueString>
	    </epdcx:statement>
	  </epdcx:description>
	</epdcx:descriptionSet>
      </xmlData>
    </mdWrap>
  </dmdSec>
</mets>
"""

def upload_multipart(connection, title, summary, language, keywords, files, unicodeEncoding='utf8'):
    # Create and zip METS file
    import zipfile
    from StringIO import StringIO

    zipFile = StringIO('')
    zipArchive = zipfile.ZipFile(zipFile, "w")
    mets = create_mets(title, summary, language, keywords)
    if isinstance(mets, unicode):
        mets = mets.encode(unicodeEncoding)
    zipArchive.writestr('mets.xml', mets)

    # Zip uploaded files
    for filename in files:
        zipArchive.writestr(filename, files[filename].read())
    zipArchive.close()

    # Send zip file to SWORD interface
    zipFile.seek(0)
    response = connection.create(payload = zipFile.read(),
                                 mimetype = "application/zip")
    """
    with open(zipFilename, "rb") as zipFile:
        response = connection.create(payload = zipFile.read(),
                                     mimetype = "application/zip")
    os.unlink(zipFilename)
    """

    # Clean-up
    return response
