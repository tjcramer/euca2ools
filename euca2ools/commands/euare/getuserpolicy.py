# Copyright 2009-2013 Eucalyptus Systems, Inc.
#
# Redistribution and use of this software in source and binary forms,
# with or without modification, are permitted provided that the following
# conditions are met:
#
#   Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
#   Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from euca2ools.commands.euare import EuareRequest, AS_ACCOUNT
import json
from requestbuilder import Arg
import urllib


class GetUserPolicy(EuareRequest):
    DESCRIPTION = "Display a user's policy"
    ARGS = [Arg('-u', '--user-name', dest='UserName', metavar='USER',
                required=True,
                help='user the poilcy is attached to (required)'),
            Arg('-p', '--policy-name', dest='PolicyName', metavar='POLICY',
                required=True, help='name of the policy to show (required)'),
            Arg('--pretty-print', action='store_true', route_to=None,
                help='reformat the policy for easier reading'),
            AS_ACCOUNT]

    def print_result(self, result):
        policy_content = urllib.unquote(result['PolicyDocument'])
        if self.args['pretty_print']:
            try:
                policy_json = json.loads(policy_content)
            except ValueError:
                self.log.debug('JSON parse error', exc_info=True)
                raise ValueError(
                    "policy '{0}' does not appear to be valid JSON"
                    .format(self.args['PolicyName']))
            policy_content = json.dumps(policy_json, indent=4)
        print policy_content
