import copy
import multiprocessing

import utils
from web.api.models import Device

class RuleParser(object):
    _services = {}
    _lock = multiprocessing.Lock()

    def get_service_settings(self, service):
        """Get rules for specific service

        Args:
            service (str): json file name for standard rules

        Returns:
            dict: service rules
        """
        if service not in self._services:
            self._services[service] = utils.get_json(
                'firewall/services/{}.json'.format(service))
        return self._services[service]

    def _add_devices_to_rule(self, rule, devices):
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
        saddr_rule['add']['rule']['expr'].insert(0, expr)
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
        daddr_rule['add']['rule']['expr'].insert(0, expr)
        return [saddr_rule, daddr_rule]
    def _add_to_service_devices(self, service_devices, service, ip):
        if(service not in service_devices):
            service_devices[service] = set()
        service_devices[service].add(ip)
        return service_devices
    def get_rules_for_devices(self):
        """Retrieve devices from database and create nf-table rules.

        Returns:
            _type_: _description_
        """
        with self._lock:
            devices = Device.query.all()
        service_devices = {}
        rules = []
        for device in devices:
            blocked_device = False
            for rule in device.rules:
                if(rule.service == 'block'):
                    blocked_device = True
                service_devices = self._add_to_service_devices(service_devices, rule.service, device.ip)
            if not blocked_device:
                local_device = False
                cloud_device = False
                for functionality in device.functionalities:
                    for service in functionality.services:
                        local_device = True
                        if service.cloud:
                            cloud_device = True
                            break
                    if service.cloud:
                        break
                service = 'block'
                if cloud_device:
                    service = 'cloud'
                elif local_device:
                    service = 'local'
                service_devices = self._add_to_service_devices(service_devices, service, device.ip)
        for service in service_devices:
            settings = self.get_service_settings(service)
            ip4_devices = list(
                filter(lambda device: utils.is_ip4(device), service_devices[service]))
            for rule in settings:
                setting_rules = self._add_devices_to_rule(rule, ip4_devices)
                rules += setting_rules
        return rules
