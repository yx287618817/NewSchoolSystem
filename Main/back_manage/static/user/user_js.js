function filter_user() {
    let user = $('#user').val();
    console.log(user);
    $.ajax({
        url: '/back_manage/user_manage/',
        type: 'GET',
        data: {'user': user},
        success: function (arg) {
            let res = JSON.parse(arg);
            if (!res){
                alert('没有这个用户');
            }
        }
    })
}