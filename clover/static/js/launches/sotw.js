$(document).ready(function () {
    update();

    setInterval(update, 1000);

    function update() {
        let now = new Date();
        let launch = new Date(1566756000000);
        var elm = $("#time");

        let diff = launch - now;
        let days = launch.getDate() - now.getDate();
        let hours = launch.getHours() - now.getHours();
        let min = launch.getMinutes() - now.getMinutes();
        let sec = launch.getSeconds() - now.getSeconds();

        if (diff <= 0) {
            elm.html("has begun!");
        } else if (days > 0) {
            elm.html("begins in " + days + " days");
        } else if (hours > 0) {
            elm.html("begins in " + hours + " hours");
        } else if (min > 0) {
            elm.html("begins in " + min + " minutes");
        } else if (sec > 0) {
            elm.html("begins in " + sec + " seconds");
        }

        console.log(diff);
    }
});