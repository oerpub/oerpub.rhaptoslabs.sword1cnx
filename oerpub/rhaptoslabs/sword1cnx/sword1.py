"""
Library for interacting with servers supporting the SWORD version 1
protocol.

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

class Connection:
    def __init__(self, url, user_name, user_pass, download_service_document=True):
        self.url = url
        self.userName = user_name
        self.userPass = user_pass

        if download_service_document:
            self.get_service_document()
        else:
            self.sd = None

    def get_service_document(self):
        import urllib2, base64
        req = urllib2.Request(self.url)
        req.add_header('Authorization', 'Basic ' + base64.b64encode(self.userName + ':' + self.userPass))
        conn = urllib2.urlopen(req)
        self.sd = conn.read()
        conn.close()

    def create(self, payload, mimetype):
        import urllib2, base64
        req = urllib2.Request(self.url)
        req.add_header('Authorization', 'Basic ' + base64.b64encode(self.userName + ':' + self.userPass))
        req.add_header('Content-type', mimetype)
        req.add_header('Content-length',  len(payload))
        conn = urllib2.urlopen(req, payload)
        result = conn.read()
        conn.close()
        return result
