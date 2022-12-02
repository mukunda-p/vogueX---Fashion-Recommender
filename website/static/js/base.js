// var formattedFormData2={};
// $(document).ready(function(){
//     $('#favourites').click(function(event) { 
//         console.log("Favourites is hit")
//     event.preventDefault(); 
//     formattedFormData2={}
//     formattedFormData2["actionToBePerformed"] = "FETCH_FAVOURITES"
//     formData = JSON.stringify(formattedFormData2)
//     console.log("Using Favourites")
//     console.log(formData)
//     event.preventDefault();
    // $.ajax({
    //     type:"POST",
    //     url:"/favourites",
    //     data:formData,
    //     success:function(){
    //         var redirectUrl = window.location.protocol + "//" + window.location.host + "/results";
    //             location.href = redirectUrl;
            
    //     },
    //     dataType: "json",
    //     contentType : "application/json"
    // })

    // const req = new XMLHttpRequest();
    // req.open("GET","/favourites.html");
    // req.addEventListener('load',function(){
    //     const res = JSON.parse(req.responseText)
    //     console.log(res)
    // })
    // req.send();
    // });

// $("#favourites").click(function(){
//     $.get("favourites.html", function(data, status){
//       alert("Data: " + data + "\nStatus: " + status);
//     });
  
// });

