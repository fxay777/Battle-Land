$(document).ready(function() {
    $(".category").click(function(elm) {
        var target = $(elm.target);
        var href = target.data("href");

        if (target.hasClass("disabled")) {
            return
        }

        window.location = href;
    });
});