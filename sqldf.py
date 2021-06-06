'''
Written by Joseph Gagliardo joey@me.com on 2021-06-05
This module is meant to offer a more flexible version of what PandaSQL does, by providing support for Python list and dict
and the ability to use Python UDF within the SQL. Furthermore, you can use SQL UPDATE, INSERT, DELETE commands to modify
the DataFrame object and return a new DataFrame with those results.

Instead of passing env = globals() all the time, instead of importing sqldf use the following function instead so you can skip passing it

def sqldf(sql: str, *, index:bool = False, env = globals(), output:str = None, **params):
    import sqldf
    return sqldf.sqldf(sql, index = index, env = globals(), output = output, **params)

'''
def sqldf(sql: str, *, index:bool = False, env = globals(), output:str = None, **params):
    '''
    sql : str
         The SQL command or commands you want to run. 
         You can pass in multiple statements separated by a ; in order to do UPDATE, INSERT, DELETE, but the last query must be a SELECT without a ;
    
    index : bool (Default: False)
         When a DataFrame is pushed into the memory table, should the index col be included

    env : dict
         The default is to pass the globals() so the function can automatically extract the table names and push them into the memory database.
         It only finds the tables referenced after a FROM or JOIN.

    output : str {'dict', 'list', 'series', 'split', 'records', 'index'}
        Determines the type of the values of the dictionary.
    
        - 'dict' (default) : dict like {column -> {index -> value}}
        - 'list' : dict like {column -> [values]}
        - 'series' : dict like {column -> Series(values)}
        - 'split' : dict like
          {'index' -> [index], 'columns' -> [columns], 'data' -> [values]}
        - 'records' : list like
          [{column -> value}, ... , {column -> value}]

    params : dict
        KV parameters to pass in python functions to the memory database, 
        key is a string which is the function name SQL will use, 
        value is a ponter to the funct
    '''

    def get_table_names(sql):
        import re
        x = re.split('from |FROM |From |join |JOIN |Join ', sql.lower())
        tables = [t[:t.index(' ')] for t in x][1:]
        return tables

    from pandas import read_sql_query, DataFrame
    import sqlite3
    import types 
    from inspect import signature


    with sqlite3.connect(':memory:') as cn:
        addedtables = set()
        # go through the list of KV parameters to push any UDF's or named tables into the memory database
        for k, v in params.items():
            if type(v) in (types.FunctionType, types.LambdaType):
                cn.create_function(k, len(signature(v).parameters), v)
            elif isinstance(v, DataFrame):
                v.to_sql(k, cn, index = index)
                addedtables.add(k)
            elif isinstance(v, dict) or isinstance(v, list):
                addedtables.add(k)
                df = DataFrame(v)
                df.to_sql(k, cn, index = index)

        # search through the environment to see if any tables mentioned in FROM or JOIN clause exist and push them into the memory database
        # the table can be a DataFrame or a list or dict that is convertible to a DataFrame
        for k in get_table_names(sql):
            if k in env and k not in addedtables:
                o = env[k]
                if isinstance(o, DataFrame):
                    o.to_sql(k, cn, index = index)
                elif isinstance(o, dict) or isinstance(o, list):
                    df = DataFrame(o)
                    df.to_sql(k, cn, index = index)



        # you can pass in multiple statements separated by a ; in order to do UPDATE, INSERT, DELETE, but the last query must be a SELECT
        if ';' in sql:
            commands = [x.strip() for x in sql.split(';')]
            for c in commands[:-1]:
                cn.execute(c)
            r = read_sql_query(commands[-1], cn)
        else:
            r = read_sql_query(sql, cn)

        # if the output flag is passed it calls the DataFrame to_dict with that option
        if output:
            return r.to_dict(output)
        
        return r
