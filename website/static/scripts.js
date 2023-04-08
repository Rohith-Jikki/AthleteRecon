$("#register").submit(function(e){
    e.preventDefault();
    var $form = $(this);
    var $error = $form.find(".error");
    var whereto = $form.find("#club-or-player").val();
    var data = $form.serialize();
    
    if(whereto == 'player'){
        var url = '/player-profile'
    }
    else{
        var url = '/clubs'
    }
    $.ajax({
        url: "/sign-up",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp){
            console.log(resp);
            window.location.href= url
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
    var whereto = $form.find("#club-or-player").val();
    var data = $form.serialize();
    if(whereto == 'player'){
        var url = '/player-profile'
    }
    else{
        var url = '/clubs'
    }

    $.ajax({
        url: "/login",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp){
            console.log(resp);
            window.location.href= url
        },
        error: function(resp){
            console.log(resp);
            $error.text(resp.responseJSON.error);
        }
    })
})