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
                if (field == "dispatch_group_name") {
                    $("#dispatch_group_button_" + gr_id).text(newName);
                }
                getGroupInfo(gr_id);
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
        url: "/api/lists/" + grId,
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
            $("#dispatch_group_button_" + grId).addClass(changeAt === "enable" ? "u-border-green" : "u-border-red")
            $("#dispatch_group_button_" + grId).removeClass(changeAt === "enable" ? "u-border-red" : "u-border-green")
            getGroupInfo(data.gr_id);
        },
        error: function () {
            alert("Не удалось обновить название, попробуйте позже");
        }
    });
};

function confirm(id) {
    $.ajax({
        type: "POST",
        url: "/api/users/confirm",
        data: JSON.stringify({"id": id}),
        success: function (data) {
            document.location = "users.html"
        },
        contentType: "application/json; charset=utf-8",
        dataType: "json"
    });
};

function block(id) {
    $.ajax({
        type: "POST",
        url: "/api/users/block",
        data: JSON.stringify({"id": id}),
        success: function (data) {
            document.location = "users.html"
        },
        contentType: "application/json; charset=utf-8",
        dataType: "json"
    });
};
