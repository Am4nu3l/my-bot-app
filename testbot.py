import mysql.connector

host = "bjlkoynqli1nvi24lvbu-mysql.services.clever-cloud.com"
user = "uokebst08hzhbrnu"
password = "rPjR6o7BweOLqMA8X41d"
database = "bjlkoynqli1nvi24lvbu"
connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database,
    port=3306,

)
if connection.is_connected():
    print("connected")
else:
    print("not connected")
