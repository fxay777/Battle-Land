$(document).ready(function() {
    $.ajax({
        type: "GET",
        url: '/api/get/player/trending',
        success: function (data) {
            console.log(data);
            if (data["success"] == true) {
                var parent = $("#trending-players");
                var players = data["data"];

                $("#sidebar-loading").hide('slow');
                
                var i = 0;
                for (let[uuid, value] of players) {
                    if (i >= 5) {
                        break;
                    }
                    $.ajax({
                        type: "GET",
                        url: '/api/player/' + uuid,
                        success: function (res) {
                            console.log(res);
                            if (res["success"] == true) {
                                player = res["data"];
                                parent.append('<div class="sidebar-content"><a href="/u/' + player["name"] + '" style="color: ' + player["color"] + ';" class="creator"><img src="https://minotar.net/avatar/' + uuid + '/16">' + player["name"] + '</a><span>' + value + '</span></div>').show('slow');
                            }
                        },
                    });
                    i++;
                }
            }
        },
    });
});