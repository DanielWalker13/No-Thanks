test = ['10', '11', '12', '13', '14', '15', '17', '19', '20', '22', '23', '24', '25', '27', '3', '31', '32', '33', '34', '35', '4', '6', '7', '9']
test.sort()
print(test)
consecutives = []
for c in test:
    remove = int(c) +1
    remove = str(remove)

    if remove in test:
        consecutives.append(remove)
consecutives.sort()
print(consecutives)

def diff(first, second):
        second = set(second)
        return [item for item in first if item not in second]
different = diff(test,consecutives)
different.sort()
print(different)
"""
for x in consecutives: 
    test.remove(x)
print(test)

"""
