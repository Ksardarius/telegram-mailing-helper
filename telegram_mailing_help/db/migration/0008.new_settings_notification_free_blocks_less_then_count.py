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
        "INSERT INTO STORAGE (key,value,description) values ('count_of_free_blocks_before_notification','5','Количество оставшихся свободных блоков, при преодолении которого нужно посылать сообщение')"),
    step(
        "UPDATE STORAGE SET description='Отправлять пользователю с указанным telegram_id оповещение, когда в какой-то группе остается менее count_of_free_blocks_before_notification - значения параметра свободных блоков' WHERE key='send_notification_only_5_blocks_left_to_telegram_id'"),
]
