function fun(self) {
        let file = $('.user_photo_update').get(0).files[0]; //获取上传的文件
        let data = new FormData();
        data.append('file', file);
        $.ajax({
            url: '/update_user_photo/',
            type: 'POST',
            data: data,
            processData: false,
            contentType: false,
        }).done(function(arg) {
            console.log(arg);
            location.reload();
        })
    }

function fun1() {
    $('.user_photo_update').click();
}

$(document).ready(function () {
    let hei1 = window.outerHeight -250;
    $('.d4').height(hei1);
    let hei2 = window.innerHeight -273;
    $('.d4d2').height(hei2);
});

