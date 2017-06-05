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


class StorageDevices(base.Resource):

    def __repr__(self):
        return "<StorageDevices: %s>" % self.name


class StorageDevicesManager(base.Manager):
    resource_class = StorageDevices

    def list(self):
        devices = self._list("/os-storage-device", 'devices')
        return devices

    def get(self, storage_id):
        device = self._get("/os-storage-device/%s" % storage_id, 'device')
        return device

    def create(self, device_name, device_type, device_version=None, comment=None):
        body = {
            "device": {
                "device_name": device_name,
                "device_version": device_version,
                "device_type": device_type,
                "comment": comment
            }
        }

        return self._create("/os-storage-device", body, "device")

    def update(self, device_id, device_name, device_type, device_version=None, comment=None):
        body = {
            "device": {
                "device_name": device_name,
                "device_version": device_version,
                "device_type": device_type,
                "comment": comment
            }
        }

        return self._update("/os-storage-device/%s" % device_id,
                            body, response_key="device")

    def delete(self, device_id):
        return self._delete("/os-storage-device/%s" % device_id)
