$(document).ready(function(){   

    $("#downloadform").validate({
        rules: {
            url: {
                required: true,
                url: true
            },
            folder: {
                required: true
            },
            title: {
                required: true
            },
        },
        messages: {
            url: "Required",
            folder: "Required",
            title: "Required"
        },


        submitHandler: function(form) {

            $('#submit').attr("disabled", true);

            $.get("/queue",{   
                folder: $("#folder").val(),   
                title: $("#title").val(),   
                url: $("#url").val(),   
            }, function(data) {   
                /* Reset all fields */
                $(':input','#downloadform')
                    .not(':button, :submit, :reset, :hidden')
                    .val('');
                $('#submit').attr("disabled", false);
                $("#message").text(data).show();
            });   
            return false;   
        },
    });

    $('#folder').ajaxError(function() {
        $('#submit').attr("disabled", false);
        $("#message").text("Oops! some error occured").show();
    });

    $('#search').keypress(function(event) {
        if (event.keyCode == '13') {
            $('#search_loader').toggleClass('loader');
            $('#search').attr("disabled", true);
            $.get("/search",{   
                search_text: $("#search").val(),   
            }, function(data) {   
                $("#search_results").html(data).show();
                $('#search').attr("disabled", false);
                $('#search_loader').toggleClass('loader');
            });   
            return false;   
            event.preventDefault();
        }
    });

});



