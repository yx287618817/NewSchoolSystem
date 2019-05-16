$(function () {
    $("#send_inform").click(function () {
        $.ajax({
            url: "/lg/index/inbox.html?send=true",
            type: 'get',
            dataType: 'json',
            success: function (data) {
                console.log(data);
                $("#show").html("当前显示"+data.length+'条');
                html = '';for (var i = 0; i < data.length; i++) {
                    inform = data[i];
                    html += '<tr class="unread">';
                    html += '<td class="hidden-xs">\n' +
                        '<div class="checkbox">\n' +
                        '<input type="checkbox" class="checkbox-mail" >\n' +
                        '<label></label>\n' +
                        '</div>\n' +
                        '</td>';
                    html += '<td class="hidden-xs">\n' +
                        '<i class="fa fa-star icon-state-warning"></i>\n' +
                        '</td>';

                    html += '<td class="hidden-xs">';
                    html += inform['send_from_dpt'];
                    html += '</td class="hidden-xs">';
                    html += '<td class="hidden-xs">' +  inform["send_from_tea"]+ '</td>';
                    html += '<td class="hidden-xs">'+inform['send_to_dpt']+'</td>';
                    html += '<td class="hidden-xs">'+inform['send_to_tea']+'</td>';
                    html += '<td class="hidden-xs">' + inform['title'] + '</td>';
                    html += '<td class="hidden-xs">' + inform['times'] + '</td>';
                    html += '</tr>'
                }$("#send").html(html);
            }
        })
    });
    $("#form_inform").click(function () {
        $.ajax({
            url: "/lg/index/inbox.html?form=true",
            type: 'get',
            dataType: 'json',
            success: function (data) {
                $("#show").html("当前显示"+data.length+'条');
                console.log(data);
                html = '';for (var i = 0; i < data.length; i++) {
                    inform = data[i];
                    html += '<tr class="unread">';
                    html += '<td class="hidden-xs">\n' +
                        '<div class="checkbox">\n' +
                        '<input type="checkbox" class="checkbox-mail" >\n' +
                        '<label></label>\n' +
                        '</div>\n' +
                        '</td>';
                    html += '<td class="hidden-xs">\n' +
                        '<i class="fa fa-star icon-state-warning"></i>\n' +
                        '</td>';

                    html += '<td class="hidden-xs">';
                    html += inform['send_from_dpt'];
                    html += '</td class="hidden-xs">';
                    html += '<td class="hidden-xs">' +  inform["send_from_tea"]+ '</td>';
                    html += '<td class="hidden-xs">'+inform['send_to_dpt']+'</td>';
                    html += '<td class="hidden-xs">'+inform['send_to_tea']+'</td>';
                    html += '<td class="hidden-xs">' + inform['title'] + '</td>';
                    html += '<td class="hidden-xs">' + inform['times'] + '</td>';
                    html += '</tr>'
                }$("#send").html(html)
            }
        })
    });
    $("#all").click(function () {
        $.ajax({
            url: "/lg/index/inbox.html?all=true",
            type: 'get',
            dataType: 'json',
            success: function (data) {
                $("#show").html("当前显示"+data.length+'条');
                console.log(data);
                html = '';for (var i = 0; i < data.length; i++) {
                    inform = data[i];
                    html += '<tr class="unread">';
                    html += '<td class="hidden-xs">\n' +
                        '<div class="checkbox">\n' +
                        '<input type="checkbox" class="checkbox-mail" >\n' +
                        '<label></label>\n' +
                        '</div>\n' +
                        '</td>';
                    html += '<td class="hidden-xs">\n' +
                        '<i class="fa fa-star icon-state-warning"></i>\n' +
                        '</td>';

                    html += '<td class="hidden-xs">';
                    html += inform['send_from_dpt'];
                    html += '</td class="hidden-xs">';
                    html += '<td class="hidden-xs">' +  inform["send_from_tea"]+ '</td>';
                    html += '<td class="hidden-xs">'+inform['send_to_dpt']+'</td>';
                    html += '<td class="hidden-xs">'+inform['send_to_tea']+'</td>';
                    html += '<td class="hidden-xs">' + inform['title'] + '</td>';
                    html += '<td class="hidden-xs">' + inform['times'] + '</td>';
                    html += '</tr>'
                }$("#send").html(html)
            }
        })
    });
    $("#dustbin").click(function () {
        $.ajax({
            url: "/lg/index/inbox.html?dustbin=true",
            type: 'get',
            dataType: 'json',
            success: function (data) {
                $("#show").html("当前显示"+data.length+'条');
                console.log(data);
                html = '';for (var i = 0; i < data.length; i++) {
                    inform = data[i];
                    html += '<tr class="unread">';
                    html += '<td class="hidden-xs">\n' +
                        '<div class="checkbox">\n' +
                        '<input type="checkbox" class="checkbox-mail" >\n' +
                        '<label></label>\n' +
                        '</div>\n' +
                        '</td>';
                    html += '<td class="hidden-xs">\n' +
                        '<i class="fa fa-star icon-state-warning"></i>\n' +
                        '</td>';

                    html += '<td class="hidden-xs">';
                    html += inform['send_from_dpt'];
                    html += '</td class="hidden-xs">';
                    html += '<td class="hidden-xs">' +  inform["send_from_tea"]+ '</td>';
                    html += '<td class="hidden-xs">'+inform['send_to_dpt']+'</td>';
                    html += '<td class="hidden-xs">'+inform['send_to_tea']+'</td>';
                    html += '<td class="hidden-xs">' + inform['title'] + '</td>';
                    html += '<td class="hidden-xs">' + inform['times'] + '</td>';
                    html += '</tr>'
                }$("#send").html(html)
            }
        })
    });

});

$(function () {
    $.ajax({
            url: "/lg/index/inbox.html?all=true",
            type: 'get',
            dataType: 'json',
            success: function (data) {
                $("#show").html("当前显示"+data.length+'条');
                html = '';for (var i = 0; i < data.length; i++) {
                    inform = data[i];
                    html += '<tr class="unread">';
                    html += '<td class="hidden-xs">\n' +
                        '<div class="checkbox">\n' +
                        '<input type="checkbox" class="checkbox-mail" >\n' +
                        '<label></label>\n' +
                        '</div>\n' +
                        '</td>';
                    html += '<td class="hidden-xs">\n' +
                        '<i class="fa fa-star icon-state-warning"></i>\n' +
                        '</td>';

                    html += '<td class="hidden-xs">';
                    html += inform['send_from_dpt'];
                    html += '</td class="hidden-xs">';
                    html += '<td class="hidden-xs">' +  inform["send_from_tea"]+ '</td>';
                    html += '<td class="hidden-xs">'+inform['send_to_dpt']+'</td>';
                    html += '<td class="hidden-xs">'+inform['send_to_tea']+'</td>';
                    html += '<td class="hidden-xs">' + inform['title'] + '</td>';
                    html += '<td class="hidden-xs">' + inform['times'] + '</td>';
                    html += '</tr>'
                }$("#send").html(html)
            }
        })
});

