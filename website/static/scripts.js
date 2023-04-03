$("#register").submit(function(e){
    e.preventDefault();
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/sign-up",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp){
            console.log(resp);
            window.location.href= "/players"
        },
        error: function(resp){
            console.log(resp);
            $error.text(resp.responseJSON.error);
        }
    })
});

$("#login").submit(function(e){
    e.preventDefault();
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/login",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp){
            console.log(resp);
            window.location.href= "/players"
        },
        error: function(resp){
            console.log(resp);
            $error.text(resp.responseJSON.error);
        }
    })
})