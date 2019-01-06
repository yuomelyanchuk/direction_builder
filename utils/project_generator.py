import json
import os
import csv
import socket


class ProjectGenerator:
    def __init__(self, project_name, edge="../routing_graph/edge.csv", vertices="../routing_graph/vertices.csv"):
        self.edge_path = edge
        self.vertices_path = vertices
        self.vertices = []
        self.edge = []
        self.port = 0
        self.get_free_port()
        self.project_name = project_name
        self.read_vertices()
        self.read_edge()
        self.directory = os.path.join('..', self.project_name)
        self.queue_names = set(['input', 'errors'])
        self.code_dir_name='code'

    def check_port(self, port):
        s = socket.socket()
        s.settimeout(1)
        try:
            s.connect(("localhost", port))
        except socket.error:
            pass
        else:
            s.close
            return False
        return port

    def get_free_port(self):
        for port in range(6000, 65000):
            if self.check_port(port):
                self.port = port
                break

    def generate_project_structure(self):
        code_dir_name =  self.code_dir_name
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
            os.makedirs(os.path.join(self.directory, code_dir_name))

        for vertices in self.vertices:
            workers_directory = os.path.join(self.directory, code_dir_name, vertices.get('worker_name'))
            if not os.path.exists(workers_directory):
                os.makedirs(workers_directory)

        for er_input in ['errors', 'input']:
            workers_directory = os.path.join(self.directory, code_dir_name, er_input)
            if not os.path.exists(workers_directory):
                os.makedirs(workers_directory)

        return self

    def generate_workers_ini_file(self):
        init_files = {}
        for vertices in self.vertices:
            init_files.update({vertices.get('worker_name'): {'name': vertices.get('worker_name')}})
            init_files[vertices.get('worker_name')].update({'type': vertices.get('worker_type')})

        for edge in self.edge:
            edge_from = edge.get('from')
            edge_to = edge.get('to')
            edge_task_result = edge.get('task_result')
            edge_message = edge.get('message')

            if edge_from not in 'input':
                self.queue_names.add(edge_from + '_' + edge_to)
                init_files[edge_to].update(
                    {'listen_queue': init_files[edge_to].get('listen_queue', []) + [edge_from + '_' + edge_to]})

                section = edge_task_result + '_' + 'section'
                if not init_files[edge_from].get(section, ''):
                    init_files[edge_from].update({section: {'send_message': [], 'message': ''}})

                init_files[edge_from].update(
                    {section: {'send_message': init_files[edge_from].get(section)['send_message'] + [edge_to]
                        , 'message': edge_message}
                     }
                )
            else:
                init_files[edge_to].update(
                    {'listen_queue': init_files[edge_to].get('listen_queue', []) + [edge_from]})

            init_files.update({'errors': {'name': 'errors', 'type': 'errors', 'listen_queue': ['errors']}})
            init_files.update({'input': {'name': 'input', 'type': 'input', 'listen_queue': ['errors']}})

            for worker , ini in init_files.items():
                with open(os.path.join(self.directory,self.code_dir_name,worker,'init.json'), 'w') as fp:
                    json.dump(ini, fp,  indent=4)

        return self

    # OrderedDict([('from', 'input'), ('to', 'wine'), ('task_result', 'always'), ('message', '')])

    def read_vertices(self):
        with open(self.vertices_path) as infile:
            reader = csv.DictReader(infile, delimiter=';')
            for row in reader:
                self.vertices.append(row)

    def read_edge(self):
        with open(self.edge_path) as infile:
            reader = csv.DictReader(infile, delimiter=';')
            for row in reader:
                self.edge.append(row)


if __name__ == "__main__":
    project = ProjectGenerator(project_name='generator_test')
    project \
        .generate_project_structure() \
        .generate_workers_ini_file()
