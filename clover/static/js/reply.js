$(document).ready(function() {
    var editingReply = null;

    $("#thread-reply-submit").click(function() {
        handleThreadReply();
    });

    $("body").delegate(".thread-reply-edit", "click", function() {
        var btn = $(this);
        var replyId = btn.data('reply');
        var parent = $("[data-id='" + replyId +"']");
        var txt = parent.find(".content");

        var modal = $("#reply-edit-modal");
        modal.find("textarea").val(txt.html().trim());
        modal.find("h5").html("Editing Reply #" + replyId);
        modal.show();
        modal.modal('show');

        editingReply = replyId;
    })

    $("body").delegate("#save-edit-reply", "click", function() {
        var replyId = editingReply;
        var parent = $("[data-id='" + replyId +"']");
        var txt = parent.find(".content");
        
        txt.html("<i class='fa fa-circle-o-notch fa-spin'></i>");
        
        var modal = $("#reply-edit-modal");
        modal.modal("hide");

        var token = modal.data("token");
        
        var content = modal.find("textarea").val();

        $.ajax({
            type: "POST",
            url: '/thread/api/reply/edit/' + replyId,
            data: {
                "content": content,
                "csrfmiddlewaretoken": token
            },
            success: function(data) {
                if (data["success"] == "true") {
                    txt.html(content)
                    parent.find(".reply-edit-time").first().html('a second ago');
                }
            },
          });
    });

    $("body").delegate(".thread-reply-delete", "click", function() {
        var btn = $(this);
        var replyId = btn.data('reply');
        var parent = $("[data-id='" + replyId +"']");
        var txt = parent.find(".content");

        var modal = $("#reply-delete-modal");
        modal.find("textarea").val(txt.html().trim());
        modal.find("h5").html("Deleting Reply #" + replyId);
        modal.show();
        modal.modal('show');

        editingReply = replyId;
    })

    $("body").delegate("#save-delete-reply", "click", function() {
        var replyId = editingReply;
        var parent = $("[data-id='" + replyId +"']");
        var txt = parent.find(".content");
        
        var modal = $("#reply-delete-modal");
        modal.modal("hide");

        var token = modal.data("token");

        $.ajax({
            type: "POST",
            url: '/thread/api/reply/delete/' + replyId,
            data: {
                "csrfmiddlewaretoken": token
            },
            success: function(data) {
                if (data["success"] == "true") {
                    var children = parent.find(".children");

                    if (children.length == 0) {
                        parent.hide("slow")
                    } else {
                        parent.find(".content").first().html("<span class='deleted'>[Deleted]</span>");
                        parent.find(".thread-reply-edit").first().hide('slow');
                        parent.find(".thread-reply-delete").first().hide('slow');
                    }
                }
            },
          });
    });

    $("body").delegate(".thread-reply-child-reply", "click", function() {
        var btn = $(this);
        var replyId = btn.data('reply');
        var parent = $("[data-id='" + replyId +"']");
        var content = parent.find(".content").first();
        
        var block = content.find('.sub-reply-create');
        if (block.length != 0) {
            var first = block.first();

            if (first.is(":visible")) {
                first.hide('slow');
            } else {
                first.show('slow');
            }
            return;
        }
        
        $.ajax({
            type: "GET",
            url: '/thread/api/partial/subreply-create/' + replyId,
            success: function(data) {
                $(data).hide().appendTo(content).show('slow');
            },
          });
    })

    $("body").delegate(".thread-sub-reply-create", "click", function() {
        var btn = $(this);
        var replyId = btn.data('reply');
        var token = btn.data('token');
        var parent = $("[data-id='" + replyId +"']");
        var content = parent.find(".thread-sub-reply-content").val();
        
        handleChildReply(replyId, token, content, btn, parent);
    });

});


function handleThreadReply() {
    var btn = $("#thread-reply").find("button");
    var elm = $("#thread-reply").find("textarea");
    var content = elm.val();
    
    var thread = elm.data("thread");
    var token = elm.data("token")

    if (!content.trim()) {
        return;
    }
    
    elm.val('');
    btn.html("<i class='fa fa-circle-o-notch fa-spin'></i>");

    $.ajax({
        type: "POST",
        url: '/thread/api/reply/create/thread',
        data: {
            "content": content,
            "thread": thread,
            "csrfmiddlewaretoken": token
        },
        success: function(data) {
            if (data["success"] == "true") {
                createReply(data["data"]);
            }
        },
      });
}

function addReplyCount() {
    var current = parseInt($("#thread-messages").html().trim());

    current++;

    $("#thread-messages").html(current)
}

function handleChildReply(replyId, token, content, btn, parent) {
    if (!content.trim()) {
        console.log("empty");
        return;
    }
    
    btn.html("<i class='fa fa-circle-o-notch fa-spin'></i>");

    $.ajax({
        type: "POST",
        url: '/thread/api/reply/create/child',
        data: {
            "content": content,
            "reply": replyId,
            "csrfmiddlewaretoken": token
        },
        success: function(data) {
            if (data["success"] == "true") {
                id = data["data"];
                
                $.ajax({
                    type: "GET",
                    url: '/thread/api/reply/get/' + id,
                    success: function(data) {
                        var childDiv = parent.find(".children").first();
                        
                        if (childDiv.length == 0) {
                            parent.find(".content-block").append("<div class='children'></div>");
                            childDiv = parent.find(".children").first();
                        }
                        
                        parent.find(".sub-reply-create").first().hide('slow');
                        $(data).hide().prependTo(childDiv).show('slow');
                        btn.html("Post Reply");
                        addReplyCount();
                    },
                  });
            }
        },
      });
}

function createReply(id) {
    var btn = $("#thread-reply").find("button");

    $.ajax({
        type: "GET",
        url: '/thread/api/reply/get/' + id,
        success: function(data) {
            $(data).hide().prependTo(".replies").show('slow');
            btn.html("Post Reply");
            addReplyCount();
        },
      });
}