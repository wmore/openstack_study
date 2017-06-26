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
    resource_class = Storages

    def list(self, storage_name=None, device_id=None,
             volume_backend_name=None, usage=None, nova_aggregate_id=None,
             status=None, detailed=False):
        url = '/storages'
        filters = []
        if storage_name:
            filters.append('storage_name={0}'.format(storage_name))
        if device_id:
            filters.append('device_id={0}'.format(device_id))
        if volume_backend_name:
            filters.append('volume_backend_name={0}'.volume_backend_name(storage_name))
        if usage:
            filters.append('usage={0}'.format(usage))
        if nova_aggregate_id:
            filters.append('nova_aggregate_id={0}'.format(nova_aggregate_id))
        if status:
            filters.append('status={0}'.format(status))
        if detailed is True:
            filters.append('detail=true')
        if len(filters) > 0:
            str_filters = '&'.join(filters)
            url = url + '?' + str_filters
        storages = self._list(url, 'storages')
        return storages

    def get(self, storage_id, detailed=False):
        storage = self._get("/storages/{storage_id}?detail={detailed}".
                            format(storage_id=storage_id, detailed=detailed),
                            'storage')
        return storage

    def create(self, storage_name, device_id, metadata, usage, nova_aggregate_id):
        body = {
            "storage": {
                "storage_name": storage_name,
                "device_id": device_id,
                "metadatas": metadata,
                "usage": usage,
                "nova_aggregate_id": nova_aggregate_id
            }
        }
        return self._create('/storages', body, 'storage')

    def update(self, storage_id, storage_name=None, device_id=None, metadatas=None):
        body = {
            "storage": {
            }
        }
        if storage_name is not None:
            body['storage']['storage_name'] = storage_name
        if device_id is not None:
            body['storage']['device_id'] = device_id
        if metadatas is not None:
            body['storage']['metadatas'] = metadatas
        return self._update('/storages/%s' % storage_id, body, 'storage')

    def delete(self, storage_id):
        return self._delete("/storages/%s" % storage_id)

    def reconfig(self, storage_id):
        resp, body = self.api.client.get("/storages/%s/reconfig" % storage_id)
        return body

    def get_count_volume_group_type(self, volume_type_ids):
        url = 'os-volume-amount'
        if volume_type_ids:
            volume_type_ids_str = ','.join(volume_type_ids)
            url = url + '?volume_type_ids=' + volume_type_ids_str
        result = self._list(url, 'volume_amount')
        return result
