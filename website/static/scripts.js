function submit_processor(form, current_url){
    var $form = form;
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
        url: current_url,
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
}

$("#register").submit(function(e){
    e.preventDefault();
    submit_processor(form=$(this), current_url="/sign-up")
})

$("#login").submit(function(e){
    e.preventDefault();
    submit_processor($(this), current_url='/login')
})

function form_submit_function(form,current_url, where_to) {
    var $form = form;
    var $error = $form.find(".error");
    var data = $form.serialize();
    
    $.ajax({
        url: current_url,
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp){
            console.log(resp);
            window.location.href= where_to
        },
        error: function(resp){
            console.log(resp);
            $error.text(resp.responseJSON.error);
        }
    })
}

$("#edit-details").submit(function(e){
    e.preventDefault();
    form_submit_function(form=$(this), current_url="/players", where_to="/player-profile")
});

$("#edit-club-details").submit(function(e){
    e.preventDefault();
    form_submit_function(form=$(this), current_url="/edit-club-profile", where_to="/clubs")
});

