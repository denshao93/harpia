import tempfile


class ProcessCbers4:

    tmp_dir = tempfile.mkdtemp()

    def __init__(self, file_path):
        
        self.file_path = file_path