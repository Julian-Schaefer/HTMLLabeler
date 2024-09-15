import json

class Dataset:
    def __init__(self):
        self.labels = []
        self.selections = {}

    def add_label(self, label):
        if label not in self.labels:
            self.labels.append(label)

    def add_selection(self, url, label, elements):
        if url not in self.selections:
            self.selections[url] = {}
        self.selections[url][label] = elements

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            json.dump({'labels': self.labels, 'selections': self.selections}, f)

    def load_from_file(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            self.labels = data['labels']
            self.selections = data['selections']



dataset = Dataset()
