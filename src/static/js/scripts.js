$("form[name=openform]").submit(function(e) {

    var $form = $(this);
    var data = $form.serialize();
    
    $.ajax({
        url: "/renewalAction",
        type: 'POST',
        data: data,
        dataType: "json",
        success: function(data) {
            console.log("here success")
            window.location = '/admin-dashboard';
        },
        error: function(data) {
            window.location = '/admin-dashboard';
        }
        })

    e.preventDefault();

});