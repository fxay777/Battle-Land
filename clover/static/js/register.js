$(document).ready(function() {
    $("#register-confirm-form").submit(function(e) {
        var p1 = $(this).find("#password").val();
        var p2 = $(this).find("#password2").val();
        
        var cancel = false;

        if (p1 != p2) {
            registerConfirmError("Passwords do not match!");
            e.preventDefault();
            return;
        }

        if (p1.length <= 3) {
            registerConfirmError("Password's to short!");
            e.preventDefault();
            return;
        }
    });

    $(".register-error .close").click(function() {
        $(".register-error").hide('slow');
    })

});

function registerConfirmError(reason) {
    $(".register-error").find("#error").html(reason);
    $(".register-error").show('slow');
}