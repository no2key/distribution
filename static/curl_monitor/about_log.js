/**
 * Created with PyCharm.
 * User: yongfengxia
 * Date: 13-7-2
 * Time: 下午8:49
 * To change this template use File | Settings | File Templates.
 */

$(function () {

    $(".operation").on("click", function (e) {
        e.preventDefault();
        var logId = $.trim($(this).siblings(".id").text());
        var req = $.ajax({
            'url': '/curl/view_log?id=' + logId
        });
        req.done(function (resp) {
            $("#logContent").empty().html(resp);
            $("#modal_view_log").modal("show");
        });
    });
});