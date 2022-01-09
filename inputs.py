from main import run

path = r'data\BBC News Summary\News Articles\entertainment\500.txt'
save_to_file = False

summary = run(path, 'lexrank', limit_type='s', limit_number=2,  contains_title=True, 
    stemmer='p')
print(summary)

# write the summary to a file
if save_to_file:
    with open(r'summary.txt', 'w') as document:
        document.write(summary)