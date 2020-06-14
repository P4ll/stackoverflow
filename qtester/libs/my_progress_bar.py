from progress.bar import Bar

class MyBar(Bar):
    message = 'Loading'
    add_info = ""
    suffix = '%(index)d/%(max)d | %(percent).1f%% - %(rem_min)d min %(get_add)s'

    @property
    def rem_min(self):
        return self.eta // 60
    
    @property
    def get_add(self):
        return self.add_info
