# Copyright (C) 2015 Hewlett-Packard Development Company, L.P.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Pools interface (v2 extension)"""

from cinderclient import base


class StorageDevice(base.Resource):
    def __repr__(self):
        return "<StorageDevices: %s>" % self.name


class StorageDeviceManager(base.Manager):
    resource_class = StorageDevice

    def list(self, device_name=None, device_type_id=None, protocol=None, use_driver=None, controller_ip=None):

        url = '/os-storage-device'
        filters = []
        if device_name:
            filters.append('device_name={0}'.format(device_name))
        if device_type_id:
            filters.append('device_type_id={0}'.format(device_type_id))
        if protocol:
            filters.append('protocol={0}'.format(protocol))
        if use_driver is not None:
            filters.append('use_driver={0}'.format(str(use_driver).lower()))
        if controller_ip:
            filters.append('controller_ip={0}'.format(controller_ip))
        if len(filters) > 0:
            str_filters = '&'.join(filters)
            url = url + '?' + str_filters
        devices = self._list(url, 'devices')
        return devices

    def get(self, type_id):
        device = self._get("/os-storage-device/%s" % type_id, 'device')
        return device

    def create(self, device_name, device_type_id, protocol, use_driver=False, controller_ip=None, user_name=None,
               password=None):
        body = {
            "device": {
                "device_name": device_name,
                "device_type_id": device_type_id,
                "protocol": protocol,
                "use_driver": use_driver
            }
        }

        if controller_ip is not None:
            body['device']['controller_ip'] = controller_ip
        if user_name is not None:
            body['device']['user_name'] = user_name
        if password is not None:
            body['device']['password'] = password

        return self._create("/os-storage-device", body, "device")

    def update(self, device_id, device_name, device_type_id, protocol, use_driver=False, controller_ip=None,
               user_name=None, password=None):
        body = {
            "device": {
                "device_name": device_name,
                "device_type_id": device_type_id,
                "protocol": protocol,
                "use_driver": use_driver
            }
        }

        if controller_ip is not None:
            body['device']['controller_ip'] = controller_ip
        if user_name is not None:
            body['device']['user_name'] = user_name
        if password is not None:
            body['device']['password'] = password

        return self._update("/os-storage-device/%s" % device_id,
                            body, response_key="device")

    def delete(self, device_id):
        return self._delete("/os-storage-device/%s" % device_id)
