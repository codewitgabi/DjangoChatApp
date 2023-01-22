var p = document.getElementById("p");
var h = document.getElementById("h");
var s = document.getElementById("s");
	
function hidePopBox () 
{
	p.style.visibility = "";
	h.style.visibility = "";
	s.style.visibility = "";
}		
		
function showPopBox(arg)
{
	if (arg.style.visibility == "")
	{
		hidePopBox();
		arg.style.visibility = "visible";
	} else {
		arg.style.visibility = "";
	}
}