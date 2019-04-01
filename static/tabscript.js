function openTab(evt, tabName) {
    var i, tabcontent, tabbutton;

    //Get all elements with class == "tabcontent" and hide them.
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
	tabcontent[i].style.display = "none";
    }

    //For all elements with class == "tabbutton", remove active class.
    tabbutton = document.getElementsByClassName("tabbutton");
    for (i = 0; i < tabbutton.length; i++) {
	tabbutton[i].className = tabbutton[i].className.replace(" active", "");
    }

    //Show current tab, and give its button the active class.
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";

    //Show output if not already shown.
    document.getElementById("Output").style.display = "block";
}
