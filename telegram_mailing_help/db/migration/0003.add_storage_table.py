from yoyo import step

steps = [
    step("CREATE TABLE STORAGE (key TEXT PRIMARY KEY, value TEXT NOT NULL);",
         "DROP TABLE STORAGE;")
]
