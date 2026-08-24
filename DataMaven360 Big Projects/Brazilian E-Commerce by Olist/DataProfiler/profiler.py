import pandas as pd


def row_count(df):
    """
    Return the number of rows and columns in a DataFrame.

    Parameters:
        df (pd.DataFrame):
            Input DataFrame.

    Returns:
        dict:
            Dictionary containing the number of rows and columns.
    """

    return {
        "rows": len(df),
        "columns": len(df.columns)
    }


def column_summary(df, sort_by="original"):
    """
    Generate summary statistics for every column in a DataFrame.

    Parameters:
        df (pd.DataFrame):
            Input DataFrame.

        sort_by (str):
            Reserved for future sorting options.

    Returns:
        pd.DataFrame:
            Summary containing:
                - Column Name
                - Data Type
                - Total Rows
                - Non-Null Count
                - Null Count
                - Null %
                - Distinct Values
    """

    total_rows = len(df)
    summary = []

    for column in df.columns:
        series = df[column]
        null_count = series.isnull().sum()

        column_info = {
            "Column": column,
            "Data Type": series.dtype,
            "Total Rows": total_rows,
            "Non-Null Count": series.count(),
            "Null Count": null_count,
            "Null %": (null_count / total_rows) * 100,
            "Distinct Values": series.nunique()
        }

        summary.append(column_info)

    summary_df = pd.DataFrame(summary)

    return summary_df


def dataset_health(df):
    """
    Generate high-level health metrics for an entire dataset.

    Parameters:
        df (pd.DataFrame):
            Input DataFrame.

    Returns:
        dict:
            Summary containing key dataset quality metrics.
    """

    row_count_summary = row_count(df)
    column_summary_df = column_summary(df)

    rows = row_count_summary["rows"]
    columns = row_count_summary["columns"]

    duplicate_rows = df.duplicated().sum()

    columns_with_nulls = len(
        column_summary_df.query("`Null Count` > 0")
    )

    completely_empty_columns = len(
        column_summary_df.query("`Null %` == 100")
    )

    potential_primary_keys = (
        column_summary_df["Distinct Values"]
        == column_summary_df["Total Rows"]
    ).sum()

    potential_date_columns = len(
        column_summary_df.query("`Data Type` == 'object'")
    )

    potential_numeric_columns = len(
        column_summary_df.query("`Data Type` == 'int64'")
    )

    potential_categorical_columns = len(
        column_summary_df.query("`Data Type` == 'string'")
    )

    health_score = None

    health_summary = {
        "Rows": rows,
        "Columns": columns,
        "Duplicate Rows": duplicate_rows,
        "Columns With Nulls": columns_with_nulls,
        "Completely Empty Columns": completely_empty_columns,
        "Potential Primary Keys": potential_primary_keys,
        "Potential Date Columns": potential_date_columns,
        "Potential Numeric Columns": potential_numeric_columns,
        "Potential Categorical Columns": potential_categorical_columns,
        "Health Score": health_score
    }

    return health_summary

def duplicate_summary(df, subset = None):
    """
    Short description: Return Dataset duplicates only.

    Parameters:
        df (DataFrame)

    Returns:
        ...
    """
    # Logic
    pass


def null_summary(df):
    """
    Short description: | Column | Null Count | Null % |

    Parameters:
        df (DataFrame)

    Returns:
        ...
    """

    # Logic
    pass

def numerical_summary(df):
    """
    Short description: | Column | Distinct Count |

    Parameters:
        df (DataFrame)

    Returns:
        ...
    """
    # Logic
    pass


#categorical_summary()
#outlier_summary()
#relationship_checks()
#dtype_summary()
#primary_key_candidates