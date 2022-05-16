from web.api.models import Device
import json
import os
import utils
import copy
class RuleParser(object):
    rules = []
    services = {}
    def get_service_settings(self, service):
        if service not in self.services:
            self.services[service] = utils.get_json('firewall/services/{}.json'.format(service))
        return self.services[service]
    def add_devices_to_rule(self, rule, devices):
        saddr_rule = copy.deepcopy(rule)
        daddr_rule = copy.deepcopy(rule.copy())
        expr = {
            "match": {
                "op": "==",
                "left": {
                    "payload": {
                        "protocol": "ip",
                        "field": "saddr"
                    }
                },
                "right": 
                    {"set": devices}
            }
        }
        saddr_rule['add']['rule']['expr'].insert(0,expr)
        expr = {
            "match": {
                "op": "==",
                "left": {
                    "payload": {
                        "protocol": "ip",
                        "field": "daddr"
                    }
                },
                "right": {"set": devices}
            }
        }
        daddr_rule['add']['rule']['expr'].insert(0,expr)
        return [saddr_rule,daddr_rule]
    def get_rules_for_devices(self):
        devices = Device.query.all()
        service_devices = {}
        rules = []
        for device in devices:
            for rule in device.rules:
                if(rule.service not in service_devices):
                    service_devices[rule.service] = []
                service_devices[rule.service].append(device.ip)
        for service in service_devices:
            settings = self.get_service_settings(service)
            ip4_devices = list(filter(lambda device: utils.is_ip4(device), service_devices[service]))
            for rule in settings:
                setting_rules = self.add_devices_to_rule(rule, ip4_devices)
                rules += setting_rules
        return rules
