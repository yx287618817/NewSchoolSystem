
!function($) {
    "use strict";

    var SweetAlert = function() {};

    //examples 
    SweetAlert.prototype.init = function() {
        
    //Basic
    $('#sa-basic').click(function(){
        swal("Here's a message!");
    });

    //A title with a text under
    $('#sa-title').click(function(){
        swal("Here's a message!", "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed lorem erat eleifend ex semper, lobortis purus sed.")
    });

    //Success Message
    $('#sa-success').click(function(){
        swal("提交成功", "", "success")
    });

    //Warning Message
    $('#sa-warning').click(function(){
        swal({   
            title: "是否确认?",
            text: "该操作不可逆",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "确认!",
            closeOnConfirm: false
        }, function(){
            swal("Deleted!", "Your imaginary file has been deleted.", "success");
        });
    });

    //Parameter
    $('#sa-params').click(function(){
        swal({
            title: "是否确认?",
            text: "该操作不可逆!",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "确认",
            cancelButtonText: "取消",
            closeOnConfirm: false,
            closeOnCancel: false
        }, function(isConfirm){
            if (isConfirm) {
                swal("提交成功", "该工作已完成", "success");
            } else {
                swal("取消", "可以继续编辑", "error");
            }
        });
    });

    //Custom Image
    $('#sa-image').click(function(){
        swal({
            title: "Title",
            text: "Lorem ipsum dolor sit amet, consectetur",
            imageUrl: "assets/images/users/avatar-1.jpg"
        });
    });

    //Auto Close Timer
    $('#sa-close').click(function(){
         swal({
            title: "Auto close alert!",
            text: "I will close in 2 seconds.",
            timer: 2000,   
            showConfirmButton: false 
        });
    });


    },
    //init
    $.SweetAlert = new SweetAlert, $.SweetAlert.Constructor = SweetAlert
}(window.jQuery),

//initializing 
function($) {
    "use strict";
    $.SweetAlert.init()
}(window.jQuery);