$(function () {

    $(".del_monitor_item").on("click", function (e) {
        var r = confirm("确定删除吗？");
        if (r) {
            var monitor_id = $.trim($(this).parent().siblings('.id').text());
            var req = $.ajax({
                url: '/curl/del_monitor?id=' + monitor_id,
                dataType: 'json'
            });
            req.done(function (resp) {
                if (resp.status === 'success') {
                    setTimeout("window.location.href='/curl/monitor_list'", 100);
                } else {
                    alert(resp.msg);
                }
            });
        }
    });

    $("#add-monitor-item").on("click", function (e) {
        $("#url-to-monitor").val("");
        $("#monitor-or-not").children("option:selected").removeAttr("selected");
        $(".ip-item>.icon-minus-sign").parent().remove();
        $("#modal-add-monitor-item").modal("show");
    });

    $(document).on("click", ".icon-plus-sign", function (e) {
        var ip_ele = $("<div></div>", {
            "class": "ip-item"
        });
        ip_ele.append($("<input />", {
            "class": 'input-large ip',
            "type": "text"
        }));
        ip_ele.append($("<i></i>", {
            "class": 'icon-minus-sign'
        }));
        $(this).parent().parent().append(ip_ele);
    });

    $(document).on("click", '.icon-minus-sign', function (e) {
        $(this).parent().remove();
    });

    $(".modify_monitor_item").on("click", function (e) {
        var parent = $(this).parent();
        $("#monitor_id_modify").html($.trim(parent.siblings(".id").text()));
        var url = $.trim(parent.siblings(".url").text());
        var ip_td = $.trim(parent.siblings(".ip_list").html()).replace(/(<(br|BR)\s*\/?>)/g, ';').replace(/;$/, '');
        var ip_list = ip_td.split(';');
        var monitor_or_not = parent.siblings(".monitor_or_not").children("option:selected").val();

        $("#url_to_monitor").val(url);

        $("#ip_list").empty();

        var len = ip_list.length;
        for (var index = 0; index < len; index++) {
            var which_icon = "icon-minus-sign";
            if (index === 0) {
                which_icon = "icon-plus-sign";
            }
            var ip_element = $("<div></div>", {
                "class": "ip-item"
            });
            ip_element.append($("<input/>", {
                "class": "input-large ip",
                "type": "text",
                "value": $.trim(ip_list[index])
            }));
            ip_element.append($("<i></i>", {
                "class": which_icon
            }));
            $("#ip_list").append(ip_element);
        }

        $("#monitor_or_not").children("option[value=" + monitor_or_not + "]").prop("selected", true);

        $("#modal-modify-monitor-item").modal("show");
    });

    $("#submit-change").on("click", function (e) {
        var csrf_token = $("#csrf_token").text();
        var id = $("#monitor_id_modify").text();
        var url = $("#url_to_monitor").val();
        var ip_list = [];
        $(".ip-item>input").each(function () {
            var ip = $.trim($(this).val());
            if (ip !== '') {
                ip_list.push(ip);
            }
        });
        var ips = ip_list.join(";");
        var monitor_or_not = $("#monitor_or_not").children("option:selected").val();

        var req = $.ajax({
            url: '/curl/modify_monitor/',
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf_token,
                id: id,
                url_to_monitor: url,
                ips: ips,
                monitor_or_not: monitor_or_not
            },
            dataType: 'json'
        });
        req.done(function (resp) {
            if (resp.status === 'success') {
                setTimeout("window.location.href='/curl/monitor_list'", 100);
            } else {
                alert(resp.msg);
            }
        });
        $("#modal-modify-monitor-item").modal("hide");
    });

    $("#sure-to-add").on("click", function (e) {
        var csrf_token = $("#csrf-token").text();
        var url = $("#url-to-monitor").val();
        var ip_list = [];
        $(".ip-item>input").each(function () {
            var ip = $.trim($(this).val());
            if (ip !== '') {
                ip_list.push(ip);
            }
        });
        var ips = ip_list.join(";");
        var monitor_or_not = $("#monitor-or-not").children("option:selected").val();

        var req = $.ajax({
            url: '/curl/add_monitor/',
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf_token,
                url_to_monitor: url,
                ips: ips,
                monitor_or_not: monitor_or_not
            },
            dataType: 'json'
        });
        req.done(function (resp) {
            if (resp.status === 'success') {
                setTimeout("window.location.href='/curl/monitor_list'", 100);
            } else {
                alert(resp.msg);
            }
        });
        $("#modal-add-monitor-item").modal("hide");
    });
});