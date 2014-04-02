from pecan import conf, expose, redirect
import requests

base_url = conf.paddles_address


class StatsController(object):

    @expose('node_stats.html')
    def nodes(self, machine_type=None):
        uri = '{base}/nodes/job_stats'.format(base=base_url)
        if machine_type:
            uri += '?machine_type=%s' % machine_type
        else:
            uri += '/'

        response = requests.get(uri)
        if response.status_code != 200:
            redirect('/errors?status_code={status}&message={msg}'.format(
                status=response.status_code, msg=response.text))

        nodes = response.json()
        statuses = ['pass', 'fail', 'dead', 'unknown', 'running']
        for name in nodes.keys():
            node = nodes[name]
            total = sum(node.values())
            node['total'] = total
            for status in statuses:
                if node.get(status) is None:
                    node[status] = 0
        return dict(
            machine_type=machine_type,
            nodes=nodes,
            count=len(nodes),
        )
