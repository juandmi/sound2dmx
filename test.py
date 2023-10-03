import re

text = "(82.00150299072266,)"
result = int(text[1:text.index('.')])
print(result)


text = "ASDFASDF(98.23141234)=ASDF"

# Use regular expression to find the first integer
match = re.search(r'\d+', text)

if match:
    result = int(match.group())
    print(result)
else:
    print("No integer found in the text.")


text = "42"

match = re.search(r'\d+', text)

if match:
    result = int(match.group())
    print(result)
else:
    print("No integer found in the text.")
