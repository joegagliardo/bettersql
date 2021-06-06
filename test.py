import pandas as pd
from pandas import read_sql_query, DataFrame

def reverse(x):
    # sample function with one parameter
    if x is not None:
        return x[::-1]

def twofun(x, y):
    # sample function with two parameters
    return x * y

names = pd.DataFrame({'id':[1, 2, 3], 'name':['Alpha', 'Beta', 'Gamma'], 'category':[1, 2, 2]})    
categories = {'id':[1, 2, 3], 'name':['One', 'Two', 'Three']}
languages = [{'id':1, 'language':'english'}, {'id':2, 'language':'italian'}]

from sqldf import sqldf

sql = '''
SELECT n.id, n.name, n.category, c.name as categoryname, reverse(n.name) as reverse, rev(c.name) as rev, twofun(n.name, n.id) as repeat 
FROM names AS n
LEFT JOIN categories AS c on n.category= c.id
'''

r = sqldf(sql, env = globals(), reverse = reverse, twofun = twofun, rev = lambda x : None if x is None else x[::-1]) 
print(r)

# alternatively you can pass in the table names as named parameters like you do for function names, this allows you to alias them to a different name
sql = '''
SELECT n.id, n.name, n.category, c.name as categoryname, reverse(n.name) as reverse, rev(c.name) as rev, twofun(n.name, n.id) as repeat 
FROM names2 AS n
LEFT JOIN categories AS c on n.category= c.id
'''
r = sqldf(sql, reverse = reverse, twofun = twofun, rev = lambda x : None if x is None else x[::-1], names2 = names, categories = categories) 
print(r)


# You could mix the two modes also, to specify some tables and have the others automatically read
r = sqldf(sql, env = globals(), reverse = reverse, twofun = twofun, rev = lambda x : None if x is None else x[::-1], names2 = names) 
print(r)

# you could also use this instead of from sqldf import sqldf as a way of avoiding having to pass env = globals() all the time
# sort of like the way we create a lambda for pysqldf in pandasql

def sqldf(sql: str, *, index:bool = False, env = globals(), output:str = None, **params):
    import sqldf
    return sqldf.sqldf(sql, index = index, env = globals(), output = output, **params)


sql = '''
update names set name = 'Omega' where id = 1;
insert into names values(4, 'Pi', 1);
SELECT n.id, n.name, n.category, c.name as categoryname, reverse(n.name) as reverse, rev(c.name) as rev, l.language
FROM names AS n
LEFT JOIN categories AS c on n.category = c.id
LEFT JOIN languages as l on n.category = l.id
'''

r = sqldf(sql, reverse = reverse, rev=lambda x : None if x is None else x[::-1])
#r = sqldf(sql, reverse = reverse, rev=lambda x : None if x is None else x[::-1], output = 'dict')
#r = sqldf(sql, reverse = reverse, rev=lambda x : None if x is None else x[::-1], output = 'records')
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

r = sqldf(sql)
print(r)

# can also output the result into modes supported by to_dict method of DataFrame
r = sqldf(sql, output = 'dict')
print(r)
r = sqldf(sql, output = 'records')
print(r)
