updateDispatchGroupButtons = function () {
    $.ajax({
        type: "GET",
        url: "/templates/dispatch_group_buttons",
        data: "",
        success: function (data) {
            $("#dispatch-group-buttons").replaceWith(data)
        }
    });
}

removeButton = function (gr_id) {
    if (confirm('Вы уверены что хотите удалить кнопку?')) {
        $.ajax({
            type: "POST",
            url: "/api/lists/" + gr_id + "/change",
            data: JSON.stringify({"hidden": true}),
            success: function (data) {
                $("#dispatch-group-info").replaceWith("<div id=\"dispatch-group-info\">Кнопка была успешно удалена</div>")
                updateDispatchGroupButtons();
            },
            error: function () {
                alert("Не удалось удалить кнопку, попробуйте позже");
            }
        });
    }
}

editObject = function (field, current, gr_id) {
    let newName = prompt("Укажите новое значение для поля", current)
    if (newName) {
        const sendData = {};
        sendData[field] = newName
        $.ajax({
            type: "POST",
            url: "/api/lists/" + gr_id + "/change",
            data: JSON.stringify(sendData),
            success: function (data) {
                getGroupInfo(gr_id);
                updateDispatchGroupButtons();
            },
            error: function () {
                alert("Не удалось обновить статус, попробуйте позже");
            }
        });
    }
};
getGroupInfo = function (grId) {
    $.ajax({
        type: "GET",
        url: "/templates/lists/" + grId,
        data: "",
        success: function (data) {
            $("#dispatch-group-info").replaceWith(data)
        }
    });
};
changeStateOfDispatchGroup = function (grId, changeAt) {
    $.ajax({
        type: "POST",
        url: "/api/lists/" + grId + "/state",
        data: JSON.stringify({"state": changeAt}),
        success: function (data) {
            getGroupInfo(data.gr_id);
            updateDispatchGroupButtons();
        },
        error: function () {
            alert("Не удалось обновить, попробуйте позже");
        }
    });
};

changeUserState = function (id) {
    $.ajax({
        type: "POST",
        url: "/api/users/state/change",
        data: JSON.stringify({"id": id}),
        success: function (data) {
            $('#user_state_' + id).html(data["localizedState"]);
        },
        contentType: "application/json; charset=utf-8",
        dataType: "json"
    });
};

changeSettings = function (key) {
    let newValue = prompt("Укажите новое значение для свойства: " + key, $('#settings-' + key).html())
    if (newValue) {
        $.ajax({
            type: "POST",
            url: "/api/settings/change",
            data: JSON.stringify({"key": key, "value": newValue}),
            success: function (data) {
                $('#settings-' + data["key"]).html(data["value"]);
            },
            contentType: "application/json; charset=utf-8",
            dataType: "json"
        });
    }
}

GLOBAL_DIRTY_STORAGE = {};
if (GLOBAL_DIRTY_STORAGE["dispathcer_group_list_of_items_messasge_counter_event"] == undefined) {
    $("#list_of_items").on('change paste', function () {
        $('#list_of_items_counter').text('Количество строк: ' + ($(this).val().split("\n").length));
    });
    GLOBAL_DIRTY_STORAGE["dispathcer_group_list_of_items_messasge_counter_event"] = true;
}
