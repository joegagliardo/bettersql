#! python3.9
import sys
print(sys.version)
import pandas as pd

# if running locally during builds before uploading to pypi
from sqldf import sqldf

# if running to test the downloaded package from pypi
# from bettersql import sqldf

def reverse(x):
    # sample function with one parameter
    if x is not None:
        return x[::-1]

def twofun(x, y):
    # sample function with two parameters
    return x * y

# DataFrame source
names = pd.DataFrame({'id':[1, 2, 3], 'name':['Alpha', 'Beta', 'Gamma'], 'category':[1, 2, 2]})    

# Dict source of lists
categories = {'id':[1, 2, 3], 'name':['One', 'Two', 'Three']}

# List of dicts as source
languages = [{'id':1, 'language':'english'}, {'id':2, 'language':'italian'}]

sql = '''
SELECT n.id, n.name, n.category, c.name as categoryname
    , reverse(n.name) as reverse, rev(c.name) as rev, twofun(n.name, n.id) as repeat 
FROM names AS n
LEFT JOIN categories AS c on n.category= c.id
'''

r = sqldf(sql, reverse = reverse, twofun = twofun, rev = lambda x : None if x is None else x[::-1]) 
print('-' * 30)
print(r)

# alternatively you can pass in the table names as named parameters like you do for function names, this allows you to alias them to a different name
sql = '''
SELECT n.id, n.name, n.category, c.name as categoryname
    , reverse(n.name) as reverse, rev(c.name) as rev, twofun(n.name, n.id) as repeat 
FROM names2 AS n
LEFT JOIN categories AS c on n.category= c.id
'''
r = sqldf(sql, reverse = reverse, twofun = twofun
        , rev = lambda x : None if x is None else x[::-1], names2 = names, categories = categories) 
print('-' * 30)
print(r)


# You could mix the two modes also, to specify some tables and have the others automatically read
r = sqldf(sql, reverse = reverse, twofun = twofun, rev = lambda x : None if x is None else x[::-1], names2 = names) 
print('-' * 30)
print(r)

sql = '''
update names set name = 'Omega' where id = 1;
insert into names values(4, 'Pi', 4);
SELECT n.id, n.name, n.category, c.name as categoryname
    , reverse(n.name) as reverse, rev(c.name) as rev, l.language
FROM names AS n
LEFT JOIN categories AS c on n.category = c.id
LEFT JOIN languages as l on n.category = l.id
'''

r = sqldf(sql, reverse = reverse, rev=lambda x : None if x is None else x[::-1])
print('-' * 30)
print(r)

# Could also create a table in the sql connection and use it for the SELECT query
sql = '''

create table other(id int, name string);
insert into other select 1, 'other' 
union all select 2, 'thing';
SELECT n.id, n.name, n.category, o.name as othername
FROM names AS n
LEFT JOIN other as o on n.category = o.id
'''

print('-' * 30)
print('DataFrame output')
r = sqldf(sql)
print(r)

print('-' * 30)
print('DataFrame output')
r = sqldf(sql, output = 'dataframe')
print(r)

# can also output the result into modes supported by to_dict method of DataFrame
print('-' * 30)
print('dict output')
r = sqldf(sql, output = 'dict')
print(r)

print('-' * 30)
r = sqldf(sql, output = 'list')
print('list output')
print(r)

print('-' * 30)
r = sqldf(sql, output = 'records')
print('records output')
print(r)
  
def inside_function():
    # Here the data sources are inside a function so they would be found in the locals() not the
    # globals() but the two environments are now merged in the sqldf function
    
    # DataFrame source
    names1 = pd.DataFrame({'id':[1, 2, 3], 'name':['Alpha', 'Beta', 'Gamma'], 'category':[1, 2, 2]})    

    # Dict source of lists
    categories1 = {'id':[1, 2, 3], 'name':['One', 'Two', 'Three']}

    sql = '''
    SELECT n.id, n.name, n.category, c.name as categoryname
        , reverse(n.name) as reverse, rev(c.name) as rev, twofun(n.name, n.id) as repeat 
    FROM names1 AS n
    LEFT JOIN categories1 AS c on n.category= c.id
    '''

    r = sqldf(sql, reverse = reverse, twofun = twofun, rev = lambda x : None if x is None else x[::-1]) 
    print('-' * 30)
    print(r)

inside_function()
