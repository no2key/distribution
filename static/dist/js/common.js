/**
 * Created with PyCharm.
 * User: shuangluo
 * Date: 13-7-3
 * Time: 上午10:46
 * To change this template use File | Settings | File Templates.
 */

function showAddAnotherPopup(href, name) {
    var win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus();
    return false;
}