from yoyo import step

steps = [
    step("CREATE INDEX dla_dispatch_list_id_index ON DISPATCH_LIST_ASSIGNS (dispatch_list_id);",
         "DROP INDEX dla_dispatch_list_id_index")
]
