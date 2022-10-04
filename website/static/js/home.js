$(document).ready(function(){
    $(".recoButton1").click(function(e){
        var formData = $('#recoForm').serializeArray();
        var formattedFormData = {};
        for(var i = 0; i < formData.length; i++){
            formattedFormData[formData[i]["name"]] = formData[i]["value"];
        }
        formData = JSON.stringify(formattedFormData)
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "/recommendations",
            data: formData,
            success: function(){},
            dataType: "json",
            contentType : "application/json"
        });
    });
});
