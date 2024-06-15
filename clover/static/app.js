$(document).ready(function () {
    const values = []

    var searchBar = $("#search");
    var parent = $("#search-parent");

    searchBar.keydown(function () {
        update();
    });

    searchBar.keyup(function () {
        update();
    });

    $("#sbar").submit(function (e) {
        e.preventDefault();
        window.location = "/u/" + searchBar.val();
    });

    function update() {
        parent.empty();
        var current = searchBar.val();

        if (current.length == 0) {
            return;
        }

        values.forEach(function (val, index) {
            if (val.toLowerCase().includes(current.toLowerCase())) {
                parent.append(`<a href='/u/${val}'>${val}</a>`)
            }
        });
    }


});