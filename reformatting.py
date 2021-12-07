import os
import re

"""directory = os.path.dirname(os.path.realpath(__file__)) + r'\data\BBC News Summary\Summaries\entertainment'
for filename in os.listdir(directory):
    abs_file_path = os.path.join(directory, filename)
    with open (abs_file_path, 'r+', encoding='utf-8') as doc:
        document = doc.read()
        doc.seek(0)
        new_document = re.sub(r'(\.)([a-zA-Z])', r'\1 \2', document)
        doc.write(new_document)
        doc.truncate()"""


total = []
i = 0
docs = 0
directory = os.path.dirname(os.path.realpath(__file__)) + r'\data\BBC News Summary\News Articles\entertainment'
for filename in os.listdir(directory):
    abs_file_path = os.path.join(directory, filename)
    with open (abs_file_path, 'r+', encoding='utf-8') as doc:
        document = doc.read()
        i += 1
        words = document.split()
        if len(words) > 1000:
            print(i)
        total.append(len(words))

print(max(total))
print(min(total))
