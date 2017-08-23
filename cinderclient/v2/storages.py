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
from cinderclient import utils
from six.moves.urllib import parse

class Storages(base.Resource):
    def __repr__(self):
        return "<Storages: %s>" % self.name


class StoragesManager(base.Manager):
    resource_class = Storages

    def list(self, storage_name=None, device_id=None,
             volume_backend_name=None, usage=None, nova_aggregate_id=None,
             status=None, detailed=False, project_ids=None):
        url = '/storages'
        filters = {}
        if storage_name:
            filters['storage_name'] = storage_name
        if device_id:
            filters['device_id'] = device_id
        if volume_backend_name:
            filters['volume_backend_name'] = volume_backend_name
        if usage:
            filters['usage'] = usage
        if nova_aggregate_id:
            filters['nova_aggregate_id'] = nova_aggregate_id
        if status:
            filters['status'] = status
        if detailed is True:
            filters['detailed'] = 'true'

        filters = utils.unicode_key_value_to_string(filters)
        if filters:
            params = sorted(filters.items(), key=lambda x: x[0])
            query_string = "?%s" % parse.urlencode(params)
            url = url + query_string

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

    def reconfig_batch(self, storage_ids):
        id_str = ','.join(storage_ids)
        resp, body = self.api.client.get("/storages/reconfig_batch?storage_ids=%s" % id_str)
        return body

    def get_hosts(self, storage_id):
        url = '/storages/%s/hosts' % storage_id
        result = self._list(url, 'hosts')
        return result

    def post_host(self, storage_id, opt_node, opt_aggregate_id):
        url = '/storages/%s/hosts' % storage_id
        body = {
            "host": {
                "opt_node": opt_node,
                "opt_aggregate_id": opt_aggregate_id
            }
        }
        return self._create(url, body, 'host')

    def delete_host(self, storage_id, opt_node, opt_aggregate_id):
        url = '/storages/%s/hosts/%s?opt_aggregate_id=%s' % (storage_id, opt_node, opt_aggregate_id)
        return self._delete(url)

    def create_storage_project(self, storage_id_list, project_id):
        url = '/os-storage-project'

        body = {
            "storage_projects": [
            ]
        }

        for s in storage_id_list:
            body['storage_projects'].append({
                "project_id": project_id,
                "storage_id": s
            })

        self.run_hooks('modify_body_for_create', body)
        resp, body = self.api.client.post(url, body=body)
        return body['storage_projects']

    def update_storage_project(self, storage_id_list, project_id):
        url = '/os-storage-project/%s' % project_id

        body = {
            "storage_ids": storage_id_list
        }

        self.run_hooks('modify_body_for_update', body)
        resp, body = self.api.client.put(url, body=body)
        return body

    def delete_storage_project(self, project_id, storage_id):
        url = '/os-storage-project/%s?storage_id=%s' % (project_id, storage_id)
        return self._delete(url)
