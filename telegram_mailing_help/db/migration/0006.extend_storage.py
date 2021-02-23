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
import shutil
from datetime import datetime

from yoyo import step

steps = [
    step("ALTER TABLE STORAGE ADD COLUMN description TEXT;"),
    step("UPDATE STORAGE SET description='Префикс сайта где находится админка (https://site.com/)' WHERE key='admin_url'"),
    step("UPDATE STORAGE SET description='Отправлять пользователю с указанным telegram_id оповещение, когда новый пользователь заходит в бот' WHERE key='send_notification_about_new_user_to_telegram_id'"),
    step("UPDATE STORAGE SET description='Текст сообщения, который выдается по команде /info' WHERE key='info_message'"),
    step("INSERT INTO STORAGE (key,value,description) values ('admin_url','','Префикс сайта где находится админка (https://site.com/)')", ignore_errors='apply'),
    step("INSERT INTO STORAGE (key,value,description) values ('send_notification_about_new_user_to_telegram_id','','Отправлять пользователю с указанным telegram_id оповещение, когда новый пользователь заходит в бот')", ignore_errors='apply'),
    step("INSERT INTO STORAGE (key,value,description) values ('info_message','Информация по боту','Текст сообщения, который выдается по команде /info')", ignore_errors='apply'),
    step("INSERT INTO STORAGE (key,value,description) values ('send_notification_only_5_blocks_left_to_telegram_id','','Отправлять пользователю с указанным telegram_id оповещение, когда в какой-то группе остается менее 5 свободных блоков')", ignore_errors='apply'),
]
