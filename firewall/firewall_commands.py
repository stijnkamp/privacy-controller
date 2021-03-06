import os
import json
import nftables

import utils
from firewall.rule_parser import RuleParser

class FirewallCommands(object):
    """The firewall commands that can be done from the Firewall queue
    """
    def __init__(self):
        self.rule_parser = RuleParser()
        self._setup_nftables()

    def _setup_nftables(self):
        self.nft = nftables.Nftables()
        self.nft.set_json_output(True)
        self.nft.set_stateless_output(False)
        self.nft.set_service_output(False)
        self.nft.set_reversedns_output(False)
        self.nft.set_numeric_proto_output(False)

    def set_standard_rules(self):
        """Write all needed rules to the nf-tables 
        """
        __location__ = os.path.realpath(os.path.join(
            os.getcwd(), os.path.dirname(__file__)))
        f = open(os.path.join(__location__, 'standard_rules.json'))
        data = json.load(f)
        rules = self.rule_parser.get_rules_for_devices()
        data["nftables"] += rules
        rc, output, error = self.nft.json_cmd(data)
        if rc != 0:
            # do proper error handling here, exceptions etc
            utils.log(f"ERROR: running json cmd: {error}")
            exit(1)

        if len(output) != 0:
            # more error control?
            utils.log(f"WARNING: output: {output}")
        utils.log("Done setting firewall")
        f.close()

    def get_firewall_rules(self):
        """Retrieve the current set of rules from the nf-tables service (`JSON structure <https://firewalld.org/2019/09/libnftables-JSON>`_)

        Returns:
            dict: A dict with all rules 
        """
        rc, output, error = self.nft.cmd("list ruleset")
        if rc != 0:
            # do proper error handling here, exceptions etc
            utils.log("ERROR: running cmd 'list ruleset'")
            utils.log(error)
            exit(1)
        if len(output) == 0:
            # more error control
            utils.log("ERROR: no output from libnftables")
            exit(0)
        data_structure = json.loads(output)
        return data_structure

    def get(self, cmd):
        func = getattr(self, cmd)
        if callable(func):
            return func
        else:
            utils.log("Command {} not found".format(cmd))
            return False
