$(document).ready(function(){
	$('#Myimg').click(function(){
  		$('#Mymodal').modal('show')
	});
	const favourites = new Set()
	$('button').click(function(){
		let buttonId=this.id;
		let idx=buttonId.slice(9);
		let imgsrc=document.getElementById("Myimg"+idx).src;
		favourites.add(imgsrc);
		console.log(favourites)
	});
	
});