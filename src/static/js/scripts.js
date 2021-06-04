var to_evaluate = [];

$("form[name=openform]").submit(function(e) {
    var $form = $(this);
    var data = $form.serializeArray();
    data.push({name: 'user_list', value: to_evaluate});
    //console.log(data);
    $.ajax({
        url: "/renewalAction",
        type: 'POST',
        dataType: "json",
        data: data,//{"users" : to_evaluate, data : data},
        success: function(data) {
            window.location = '/admin-dashboard';
        },
        error: function(data) {
            window.location = '/admin-dashboard';
        }
    })
    e.preventDefault();

});


$("form[name=userform]").submit(function(e) {
    var $form = $(this);
    var data = $form.serialize();

    $('#openform').trigger('submit');

    $.ajax({
        url: "/renewalAction",
        type: 'POST',
        data: {"users" : to_evaluate},
        success: function(data) {
            window.location = '/admin-dashboard';
        },
        error: function(data) {
            window.location = '/admin-dashboard';
        }
    })
   
    e.preventDefault();

});


$(document).ready(function(){
    $("select.form").change(function(){

        var selectedForm = $(this).children("option:selected").val();
        //console.log(selectedForm);
        if (selectedForm == "Renewal Evaluation") {
            $("#to_be_evaluated").hide();
            //$("#button2").hide();
        } 
        else if (selectedForm == "Tenural Evaluation") {
            $("#to_be_evaluated").show();
            //$("#button1").hide();
            //$("#button2").show();
        }
        //alert("You have selected the country - " + selectedCountry);
    });
});


$(document).ready(function() {
    $('.userButton').click(function() {

        
        var name = $(this).attr("name");
        var email = $(this).attr("id");

        var id = $(this).attr("value");
        var stringNum = id.toString();
        var userId = "#userid";
        var res = userId.concat(stringNum);

        to_evaluate.push(id);

        //var cont = info.split(" ");
        //console.log(email)
        $('#dataTableShow > tbody:last-child').append('<tr><td>' + name + '</td><td>' + email +'</td></tr>');
        


        $(res).hide();
        //console.log("container: " + to_evaluate);
    });
});


