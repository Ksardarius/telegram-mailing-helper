<div id="dispatch-group-info">
    <ul class="u-text u-text-1">
        <li>Название: {{data["info"].dispatch_group_name}}</li>
        <li>Описание: {{data["info"].description}}</li>
        <li>Количество блоков: {{data["info"].count}}</li>
        <li>Кол-во назначенных блоков: {{data["info"].assigned_count}}</li>
        <li>Кол-во свободных блоков: {{data["info"].free_count}}</li>
    </ul>
    <a href="#" onclick="changeStateOfDispatchGroup('{{data["info"].dispatch_group_name}}','{{data["state"]["value"]}}')">{{data["state"]["text"]}}</a>
</div>