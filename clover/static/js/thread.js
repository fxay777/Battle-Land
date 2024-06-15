var editingTitle = false;
var editingContent = false;

$(document).ready(function () {
    $("#title").click(function () {
        processEditStart('title');
    });
    $("#title").keypress(function (e) {
        if (e.which == 13) {
            e.preventDefault();
            $(this).focusout();
        }
    });

    $("#title").on("focusout", function () {
        processEditStop('title');
    });

    $("#thread-txt").click(function () {
        processEditStart('content');
    });

    $("#thread-txt").on("focusout", function () {
        processEditStop('content');
    });
});

function processEditStart(type) {
    if (type == 'title') {
        editingTitle = true;
    } else if (type == 'content') {
        editingContent = true;
    }

    var ind = $("#saving-indicator");

    if (!ind.is(":visible")) {
        ind.html("Editing <i class='fa fa-circle-o-notch fa-spin'></i>")
        ind.show("slow");
    }
}

function processEditStop(type) {
    if (type == 'title') {
        editingTitle = false;
    } else if (type == 'content') {
        editingContent = false;
    }

    if (!editingTitle && !editingContent) {
        var contentElm = $("#thread-txt");
        var thread = contentElm.data("thread");
        var title = $("#title").html().trim();
        var content = getTxt(document.getElementById("thread-txt")).trim();
        var token = contentElm.data("token");

        var ind = $("#saving-indicator");

        ind.html("Saving <i class='fa fa-circle-o-notch fa-spin'></i>")
        ind.show("slow");

        $.ajax({
            type: "POST",
            url: '/thread/api/thread/edit/' + thread,
            data: {
                "content": content,
                "title": title,
                "csrfmiddlewaretoken": token
            },
            success: function (data) {
                if (data["success"] == "true") {
                    ind.html("Saved");
                    ind.delay(600).hide('slow');
                    $("#thread-edit-time").html("a second ago");
                }
            },
        });
    }
}

function getTxt(div) {
    var innerText = div.innerText
    if (innerText[innerText.length - 1] === '\n') {
        innerText = innerText.slice(0, -1)
    }
    return innerText
}