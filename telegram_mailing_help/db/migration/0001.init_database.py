from yoyo import step

steps = [
    step(
        "CREATE TABLE DISPATCH_LIST (id INTEGER PRIMARY KEY, dispatch_group_name TEXT NOT NULL, links_values_butch TEXT, description TEXT, created TEXT, is_assigned BOOLEAN);",
        "DROP TABLE DISPATCH_LIST;"),
    step("CREATE INDEX dispatch_group_name_index on DISPATCH_LIST (dispatch_group_name, created);",
         "DROP INDEX dispatch_group_name_index;"),
    step("CREATE TABLE USERS (id INTEGER PRIMARY KEY, telegram_id TEXT, name TEXT, state TEXT, created TEXT);",
         "DROP TABLE USERS"),
    step("CREATE UNIQUE INDEX telegram_id_index on USERS (telegram_id);",
         "DROP INDEX telegram_id_index"),
    step("CREATE TABLE DISPATCH_LIST_ASSIGNS (id INTEGER PRIMARY KEY, dispatch_list_id INTEGER, users_id INTEGER, state TEXT, change_date TEXT);",
         "DROP TABLE DISPATCH_LIST_ASSIGNS")
]
