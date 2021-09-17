import os
import re

directory = os.path.dirname(os.path.realpath(__file__)) + r'\data\BBC News Summary\Summaries\entertainment'
for filename in os.listdir(directory):
    abs_file_path = os.path.join(directory, filename)
    with open (abs_file_path, 'r+', encoding='utf-8') as doc:
        document = doc.read()
        doc.seek(0)
        new_document = re.sub(r'(\.)([a-zA-Z])', r'\1 \2', document)
        doc.write(new_document)
        doc.truncate()





