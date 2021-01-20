<div id="dispatch-group-info">
    <ul class="u-text u-text-1">
        <li>Название: {{data["info"].dispatch_group_name}} -> <a href="#a" onclick="editObject('dispatch_group_name','{{data["info"].dispatch_group_name}}', {{data["info"].id}})">Редактировать</a></li>
        <li>Описание: {{data["info"].description}} -> <a href="#a" onclick="editObject('description','{{data["info"].description}}', {{data["info"].id}})">Редактировать</a></li>
        <li>Количество блоков: {{data["info"].count}}</li>
        <li>Кол-во назначенных блоков: {{data["info"].assigned_count}}</li>
        <li>Кол-во свободных блоков: {{data["info"].free_count}}</li>
    </ul>
    <a href="#a" onclick="changeStateOfDispatchGroup('{{data["info"].id}}','{{data["state"]["value"]}}')">{{data["state"]["text"]}}</a>
</div>