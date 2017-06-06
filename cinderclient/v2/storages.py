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


class Storages(base.Resource):
    def __repr__(self):
        return "<Storages: %s>" % self.name


class StoragesManager(base.Manager):
    """Manage :class:`Pool` resources."""
    resource_class = Storages

    def list(self, detailed=False):
        """Lists all

        :rtype: list of :class:`Pool`
        """
        if detailed is True:
            storages = self._list("/storages?detail=True", 'storages')
            return storages
        else:
            storages = self._list("/storages", "storages")
            return storages

    def get(self, storage_id, detailed=False):
        storage = self._get("/storages/{storage_id}?detail={detailed}".format(storage_id=storage_id, detailed=detailed),
                            'storage')
        return storage

    def create(self, storage_name, storage_device, metadata):
        body = {
            "storage": {
                "storage_name": storage_name,
                "storage_device": storage_device,
                "metadatas": metadata
            }
        }
        return self._create('/storages', body, 'storage')

    def update(self, storage_id, storage_name, storage_device, metadata):
        body = {
            "storage": {
                "storage_name": storage_name,
                "storage_device": storage_device,
                "metadatas": metadata
            }
        }
        return self._update('/storages/%s' % storage_id, body, 'storage')

    def delete(self, storage_id):
        return self._delete("/storages/%s" % storage_id)

    def reconfig(self, storage_id):
        resp, body = self.api.client.get("/storages/%s/reconfig" % storage_id)
        return body
