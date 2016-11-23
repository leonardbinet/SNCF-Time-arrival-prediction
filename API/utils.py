def flatten_columns(df, columns_list, drop=False):
    """
    Goal: flatten a dataframe, which has columns filled with lists or dictionnaries.

    Parameters:
    - df : dataframe: the dataframe you want to flatten
    - columns_list: list of strings: the columns you want to flatten
    - drop: boolean: to drop flattened columns

    Dataframe is changed in place, with new columns, and flattened columns deleted if drop=True.
    Returns added columns
    """
    real_columns = df.columns
    for column in columns_list:
        if column not in real_columns:
            print("Column " + column + " is not a real column in the dataframe.")
            columns_list.remove(column)
    added_columns = []
    for column_flattened in columns_list:
        print("-" * 20)
        print("FLATTENING " + column_flattened.capitalize())
        # find out whether the value is a dict
        if isinstance(df[column_flattened][0], dict):
            # we find keys on the dictionnary
            keys_to_flatten = list(df[column_flattened][0].keys())
            # we assume that they are the same on all rows
            # TODO we could check it
            for key in keys_to_flatten:
                df[column_flattened + "_" +
                    key] = df[column_flattened].apply(lambda x: x[key])
                added_columns.append(column_flattened + "_" + key)
                print("Created column : " + column_flattened + "_" + key)
            if drop:
                df.drop(column_flattened, axis=1, inplace=True)
                print("Removed original " + column_flattened)
        # we check if it is a list
        elif isinstance(df[column_flattened][0], list):
            print("Column " + column_flattened + " is a list.")
            # check if all of same size
            diff_sizes = df[column_flattened].apply(
                lambda x: len(x)).value_counts().index.values
            print("Counts of different sizes: ", diff_sizes)
            # if all of same size
            if len(diff_sizes) == 1:
                print("All of same size: " + str(diff_sizes[0]))
                # and if size is one: we can flatten list [x] -> x
                if diff_sizes == 1:
                    print("All lists are from size one, so we can take flatten it.")
                    df[column_flattened] = df[
                        column_flattened].apply(lambda x: x[0])
                    added_columns.append(column_flattened)
                    print("Replaced column " + column_flattened)
            else:
                print(
                    "Size are not the same or >1 so we cannot flatten list, but we can count the number of elements.")
                df[column_flattened +
                    "_size"] = df[column_flattened].apply(lambda x: len(x))
                added_columns.append(column_flattened + "_size")
                print("New column: " + column_flattened + "_size")
        else:
            print("Column " + column_flattened +
                  " is not a dictionnary nor a list!")
    return added_columns


def flatten_dataframe(df, drop=False, max_depth=3):
    """
    Flatten all columns of a given dataframe, with a max_depth defined.
    """
    cols_to_flatten = df.columns
    cols_flattened = []
    k = 1
    while k <= max_depth:
        print("-" * 30)
        print("FLATENNING LEVEL " + str(k))
        print("-" * 30)
        # we use new columns to flatten them
        cols_to_flatten = flatten_columns(df, cols_to_flatten, drop)
        cols_flattened.append(cols_to_flatten)
        k += 1
        if len(cols_to_flatten) == 0:
            print("-" * 30)
            print("END NO MORE COLUMNS TO FLATTEN")
            print("-" * 30)
            break
    return cols_flattened
