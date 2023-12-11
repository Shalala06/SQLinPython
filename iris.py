import pandas as pd
import pyodbc

df = pd.read_csv("iris.csv")
# print(df.head(3))

server = 'localhost,1433'
database = 'iris1'
username = 'SA'
password = 'Coc123-4wegfbdhhdsT*5'

cnxn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=' + server +
    ';DATABASE=' + database +
    ';UID=' + username +
    ';PWD=' + password)
cursor = cnxn.cursor()

cursor.execute(
    """
     DROP TABLE IF EXISTS Iris;

     CREATE Table Iris (
         sepal_length DECIMAL(8,2) NOT NUll,
         sepal_width DECIMAL(8,2) NOT NULL,
         petal_length DECIMAL(8,2) NOT NULL,
         petal_width DECIMAL(8,2) NOT NULL,
         variety VARCHAR(MAX) NOT NUll
     );

     """
)

for index, row in df.iterrows():
    cursor.execute("INSERT INTO Iris (sepal_length,sepal_width,petal_length,petal_width,variety) values(?,?,?,?,?)",
                   row['sepal.length'], row['sepal.width'], row['petal.length'], row['petal.width'], row['variety'])

result = cursor.execute(
    """
    SELECT variety, Count(*) AS "Count By Species"
    From Iris
    GROUP By Variety
    """
).fetchall()

result_df = pd.DataFrame(result)
print(result_df)

result_df.to_csv('result.txt', sep='\t', index=False)


# file = open("result.txt", "r+")
# file.write("My first line")
# file.close()



# size = cursor.execute(
#     """
#     SELECT variety, AVG(sepal_length*sepal_width) AS "Relative Sepal Area", AVG(petal_length*petal_width) AS "Relative Petal Area"
#     From Iris
#     GROUP By Variety
#     """
# ).fetchall()
# print(size)



cursor.commit()
cursor.close()
cnxn.close()