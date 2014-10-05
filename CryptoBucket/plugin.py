###
# Copyright (c) 2014, Tyler Willis
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks

from urllib2 import urlopen
import json
import urllib2

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0')]
urllib2.install_opener(opener)

# CryptoBucket API version as of writing: 1.2
class CryptoBucket(callbacks.Plugin):
    """Plugin for accessing the CryptoBucket API."""
    threaded = True
    
    def _getapi(self, params):
		url = 'http://cryptobucket.com/api.php?' + params
		try:
			data = json.loads(urlopen(url, timeout=5).read())
		except:
			data = None
		return data
		
    def user(self, irc, msg, args, username):
		"""<username>
		
		Gets info about <username> on CryptoBucket."""
		params = 't=u&q=' + username
		data = self._getapi(params)
		if data is None:
			irc.error("Could not retrieve data.")
			return
		irc.reply("%s (%s %s) on CryptoBucket - http://cryptobucket.com/index.php?a=profile&u=%s"
			% (data['data']['username'], data['data']['first_name'],
			data['data']['last_name'], data['data']['username']))
    user = wrap(user, ['something'])
    
    def status(self, irc, msg, args, username):
		"""<username>
		
		Get the last status posted by <username>"""
		params = 't=m&q=' + username
		data = self._getapi(params)
		try:
			last_status = data['data'][0]
		except:
			irc.error("Could not retrieve status info.")
		irc.reply( ("By %s at %s: %s" % (username, last_status['time'], last_status['message'])).replace('\r\n', ''))
    status = wrap(status, ['something'])
		


Class = CryptoBucket


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
