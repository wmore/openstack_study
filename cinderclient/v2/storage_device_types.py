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


class StorageDeviceTypes(base.Resource):

    def __repr__(self):
        return "<StorageDeviceTypes: %s>" % self.name


class StorageDeviceTypesManager(base.Manager):
    resource_class = StorageDeviceTypes

    def list(self):
        devices = self._list("/os-storage-device-type", 'device_types')
        return devices

    def get(self, type_id):
        device = self._get("/os-storage-device-type/%s" % type_id, 'device_type')
        return device

    def create(self, device_type_name, vendor, device_version=None, comment=None):
        body = {
            "device_type": {
                "device_type_name": device_type_name,
                "device_version": device_version,
                "vendor": vendor,
                "comment": comment
            }
        }

        return self._create("/os-storage-device-type", body, "device_type")

    def update(self, device_id, device_type_name=None, vendor=None, device_version=None, comment=None):
        body = {
            "device_type": {
            }
        }

        if device_type_name is not None:
            body['device_type']['device_type_name'] = device_type_name

        if vendor is not None:
            body['device_type']['vendor'] = vendor

        if device_version is not None:
            body['device_type']['device_version'] = vendor

        if comment is not None:
            body['device_type']['comment'] = vendor

        return self._update("/os-storage-device-type/%s" % device_id,
                            body, response_key="device_type")

    def delete(self, device_id):
        return self._delete("/os-storage-device-type/%s" % device_id)
