import pandas as pd
from tableauhyperapi import HyperProcess, Connection, TableDefinition, SqlType, Inserter, TableName, CreateMode, Telemetry

CSV_PATH = 'sample_data.csv'
HYPER_PATH = 'sample.hyper'

def csv_to_hyper(csv_path: str, hyper_path: str):
    df = pd.read_csv(csv_path)

    # Map pandas dtypes to Hyper SqlType (simple mapping for demo)
    columns = []
    for col, dtype in df.dtypes.items():
        if pd.api.types.is_integer_dtype(dtype):
            sql_type = SqlType.int()
        elif pd.api.types.is_float_dtype(dtype):
            sql_type = SqlType.double()
        else:
            sql_type = SqlType.text()
        columns.append((col, sql_type))

    with HyperProcess(Telemetry.SEND_USAGE_DATA_TO_TABLEAU) as hyper:
        with Connection(endpoint=hyper.endpoint, database=hyper_path, create_mode=CreateMode.CREATE_AND_REPLACE) as connection:
            # Ensure the schema exists (Hyper requires the schema to be present)
            schema_name = 'Extract'
            try:
                connection.catalog.create_schema(schema_name)
            except Exception:
                # If schema already exists, ignore the error
                pass

            table = TableDefinition(table_name=TableName(schema_name, 'Extract'))
            for name, sql_type in columns:
                # Add columns to the table definition
                table.add_column(TableDefinition.Column(name, sql_type))

            # Create the table in the Hyper file
            connection.catalog.create_table(table)

            rows = [tuple(x) for x in df.itertuples(index=False, name=None)]
            with Inserter(connection, table) as inserter:
                inserter.add_rows(rows)
                inserter.execute()

if __name__ == '__main__':
    csv_to_hyper(CSV_PATH, HYPER_PATH)
    print(f'Created {HYPER_PATH} from {CSV_PATH}')
