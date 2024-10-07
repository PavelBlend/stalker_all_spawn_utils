def read_file(file_path):
    with open(file_path, 'rb') as file:
        file_data = file.read()
    return file_data
