
$(document).ready(
    function () {
        $(".middle").css({
            "height": $(window).height()-$(".top").height() + "px"
        });
    }
);

$(window).resize(function () {
    $(".middle").css({
        "height": $(window).height() - $(".top").height() + "px"
    })
});