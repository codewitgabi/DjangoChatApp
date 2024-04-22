let p = document.getElementById("p");
let h = document.getElementById("h");
let s = document.getElementById("s");
let a = document.getElementById("a");

function hidePopBox() {
  p.style.visibility = "";
  h.style.visibility = "";
  s.style.visibility = "";
  a.style.visibility = "";
}

function showPopBox(arg) {
  if (arg.style.visibility == "") {
    hidePopBox();
    arg.style.visibility = "visible";
  } else {
    arg.style.visibility = "";
  }
}
