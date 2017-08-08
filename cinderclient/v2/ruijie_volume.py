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

from volumes import VolumeManager


class RuijieVolumeManager(VolumeManager):
    def _action(self, action, volume, info=None, **kwargs):
        """Perform a volume "action."
        """
        body = {action: info}
        url = '/volumes/%s/action' % volume
        resp, body = self.api.client.post(url, body=body)
        return body


    def attach(self, volume, host_name=None):
        """Set attachment metadata.

        :param volume: The :class:`Volume` (or its ID)
                       you would like to attach.
        :param host_name: name of the attaching host.
        """
        if host_name is not None:
            req_body = {'hostname': host_name}
        body = self._action('os-ruijie_volume_attach', volume, req_body)
        result = {
            'volume_id': volume,
            'host_name': host_name,
            'volume_device_path': body['device']['path']
        }
        return result

    def detach(self, volume):
        """Set attachment metadata.

        :param volume: The :class:`Volume` (or its ID)
                       you would like to attach.
        :param host_name: name of the attaching host.
        """
        body = self._action('os-ruijie_volume_detach', volume, {})

        result = {
            'volume_id': volume,
            'volume_device_path': body['device']['path']
        }

        return result

    def update_volume_project(self, volume_id, project_id):
        url = '/os-volume-project/%s' % volume_id

        body = {
            'volume_project': {
                'project_id': project_id
            }
        }

        self.run_hooks('modify_body_for_update', body)
        resp, body = self.api.client.put(url, body=body)
        body['volume_project'].update({'volume_id': volume_id})
        return body['volume_project']
