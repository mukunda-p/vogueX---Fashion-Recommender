var formattedFormData = {};
const serpApiKey = "4f0e88cd837468e305e164834844f31e5c2f4e704e16003d2cdf1b3e10abd6a9"; 

$(document).ready(function(){
    $(".recoButton1").click(function(e){
        e.preventDefault();
        
        var formData = $('#recoForm').serializeArray();
        for(var i = 0; i < formData.length; i++){
            formattedFormData[formData[i]["name"]] = formData[i]["value"];
        }
        
        console.log("Form Data:", formattedFormData);
        var occasionValue = formattedFormData["occasion"];
        var cityValue = formattedFormData["city"];
        
        localStorage.setItem("occasionVal", occasionValue);
        localStorage.setItem("cityVal", cityValue);
        
        $.ajax({
            type: "POST",
            url: "/recommendations",
            data: JSON.stringify(formattedFormData),
            success: function(data) {
                var str = "";
                for(var i = 0; i < data["links"].length; i++){
                    str += data["links"][i] + " || ";
                }
                console.log("Recommendation Links:", data["links"]);

                var redirectUrl = window.location.protocol + "//" + window.location.host + "/results?" + str;
                location.href = redirectUrl;
            },
            dataType: "json",
            contentType: "application/json"
        });

        var query = `${occasionValue}outfit ${cityValue}`;
        $.ajax({
            type: "POST",
            url: "/recommendations",
            data: formData,
            success: function(data){
                localStorage.setItem("links", JSON.stringify(data.links));
                localStorage.setItem("imageUrls", JSON.stringify(data.imageUrls));
                
                location.href = "/result.html";
            },
            dataType: "json",
            contentType: "application/json"
        });
        
        $(".recoButton1").click(function(){
            var loader = document.getElementById('center');
            loader.style.display = '';
        });
    });
});
