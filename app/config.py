DATABASE_URI = "mysql://{mysql_user}:{mysql_passwd}@{host}/{mysql_schema}".format(
    mysql_user="webapp",
    mysql_passwd="webapp_no_password",
    # host="172.18.0.2",
    host="127.0.0.1",
    mysql_schema="webapp",
)
