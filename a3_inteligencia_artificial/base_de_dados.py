import pandas as pd
import mysql.connector
import numpy as np

db_host = "localhost"
db_user = "root"
db_password = "Aug300905dam@"
db_name = "med_vet"


table_name = "Diagnosticos"

excel_file_path = 'C:/Users/Augus/Documents/GitHub/med_vet/a3_inteligencia_artificial/bancodedados.xlsx' #Troca o diretorio

conn = mysql.connector.connect(host=db_host,port=3333, user=db_user, password=db_password, database=db_name)

cursor = conn.cursor()

new_column_names = [
    'Diagnostico', 'Eritrocitos', 'Hemoglobina', 'Hematocrito', 'HCM',
    'VGM', 'CHGM', 'Metarrubricitos', 'Proteina_Plasmatica', 'Leucocitos',
    'Leucograma', 'Segmentados', 'Bastonetes', 'Blastos', 'Metamielocitos',
    'Mielocitos', 'Linfocitos', 'Monocitos', 'Eosinofilos', 'Basofilos', 'Plaquetas'
]

df_original = pd.read_excel(excel_file_path)

df_original.columns = new_column_names

df_original.replace({np.nan: None}, inplace=True)

new_excel_file_path = 'C:/Users/Augus/Documents/GitHub/med_vet/a3_inteligencia_artificial/newdb.xlsx'
df_original.to_excel(new_excel_file_path, index=False)

create_table_query = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    Diagnostico VARCHAR(255),
    Eritrocitos DOUBLE,
    Hemoglobina DOUBLE,
    Hematocrito DOUBLE,
    HCM DOUBLE,
    VGM DOUBLE,
    CHGM DOUBLE,
    Metarrubricitos DOUBLE,
    Proteina_Plasmatica DOUBLE,
    Leucocitos DOUBLE,
    Leucograma DOUBLE,
    Segmentados DOUBLE,
    Bastonetes DOUBLE,
    Blastos DOUBLE,
    Metamielocitos DOUBLE,
    Mielocitos DOUBLE,
    Linfocitos DOUBLE,
    Monocitos DOUBLE,
    Eosinofilos DOUBLE,
    Basofilos DOUBLE,
    Plaquetas DOUBLE
);
"""
cursor.execute(create_table_query)

conn.commit()

chunk_size = 1000
for sheet_name in pd.ExcelFile(new_excel_file_path).sheet_names:
    start_row = 0
    end_row = start_row + chunk_size
    while True:
        chunk = pd.read_excel(new_excel_file_path, sheet_name, skiprows=range(1, start_row), nrows=chunk_size)
        
        if chunk.empty:
            break  

        chunk.replace({np.nan: None}, inplace=True)

        data_to_insert = [tuple(row) for row in chunk.itertuples(index=False)]

        insert_query = f"INSERT INTO {table_name} ({', '.join(chunk.columns)}) VALUES ({', '.join(['%s' for _ in range(len(chunk.columns))])})"

        cursor.executemany(insert_query, data_to_insert)

        start_row = end_row
        end_row += chunk_size

conn.commit()
conn.close()
