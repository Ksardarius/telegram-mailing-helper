# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
from yoyo import step

steps = [
    step(
        "CREATE TABLE DISPATCH_LIST (id INTEGER PRIMARY KEY, dispatch_group_name TEXT NOT NULL, links_values_butch TEXT, description TEXT, created TEXT, enabled BOOLEAN, _check_sum TEXT, _version INTEGER NOT NULL, is_assigned BOOLEAN);",
        "DROP TABLE DISPATCH_LIST;"),
    step("CREATE INDEX dispatch_group_name_index on DISPATCH_LIST (dispatch_group_name, created);",
         "DROP INDEX dispatch_group_name_index;"),
    step("CREATE UNIQUE INDEX check_sum_dispatch_list_index on DISPATCH_LIST (_check_sum);",
         "DROP INDEX check_sum_dispatch_list_index;"),
    step("CREATE TABLE USERS (id INTEGER PRIMARY KEY, telegram_id TEXT, name TEXT, state TEXT, created TEXT);",
         "DROP TABLE USERS"),
    step("CREATE UNIQUE INDEX telegram_id_index on USERS (telegram_id);",
         "DROP INDEX telegram_id_index"),
    step("CREATE TABLE DISPATCH_LIST_ASSIGNS (uuid TEXT PRIMARY KEY, dispatch_list_id INTEGER, users_id INTEGER, state TEXT, change_date TEXT);",
         "DROP TABLE DISPATCH_LIST_ASSIGNS")
]
