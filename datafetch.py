# Single Value
    # Filter (Indivitual) (What is my pending balance?) X
    # Derive (Create new thing using exist field) (What is my fee after concession?) X
    # Agg (How many students have to pay fees yet?)

# Report 
    # Filter (Common) (Term wise payment report)
    # Top or Least N
    # Pivot (group by report)
    # Order BY query


# Column Define
# Agg fn classify
# Condition classify
# Join query (How to handle multiple things)



def user_validation(Module, primary_key_column,primary_key):
    query = f"with CTE as (select * from Module where {primary_key_column} = {primary_key}) select * from CTE"
    return query


# For Personal_Record
def individual_query(name, module, column):
    view = f"SELECT {column}"
    table = f"FROM {module}"
    base_condition = f"WHERE Name = {name}"
    query = f"{view} {table} {base_condition};"
    return query


# For derive record
def derive_query(name,module,column1, column2, operation):
    view = f"SELECT {column1} {operation} {column2}"
    table = f"FROM {module}"
    base_condition = f"WHERE Name = {name}"
    query = f"{view} {table} {base_condition}"
    return query


# For doing some aggregation operations to get the single aggregated value 
def aggregation(module, agg_fn,action,condition_column):
    view = f"SELECT {agg_fn}(*)"
    table = f"FROM {module}"
    condition_ = f"where {condition_column}"
    if "pending" in action:
        condition_P = f"{condition_} != 'paid'"
        query = f"{view} {table} {condition_P}"
    elif "completed" in action:
        condition_C = f"{condition_} = 'paid'"
        query = f"{view} {table} {condition_C}"
    else:
        # Default condition or error handling
        query = f"{view} {table}"
    return query


# This is about to filter the data based on some condition only
def common_filter_query(module, condition_column, condition_value):
    view = "SELECT *"
    table = f"FROM {module}"
    base_condition = f"WHERE {condition_column} = '{condition_value}'"
    query = f"{view} {table} {base_condition}"
    return query


# This is for sort the data based on some column
def orderby(query, order_by_column, order, limit=False, n=None):
    if "limit" in query.lower():
        query = query.split(' LIMIT ')[0]
    
    order_condition = f"{query} ORDER BY {order_by_column} {order}" if order_by_column and order else query

    if limit and n:
        order_condition += f" LIMIT {n}"
    return order_condition



# This is about to limit the N number of records for limit the view
def limit(query,n):
    query = f"{query} LIMIT {n}"
    return query



def pivot_query(module, group_by_column, agg_column, agg_function):
    view = f"SELECT {group_by_column}, {agg_function}({agg_column})"
    table = f"FROM {module}"
    group_by_condition = f"GROUP BY {group_by_column}"
    query = f"{view} {table} {group_by_condition};"
    return query

