$(document).ready(function () {
    //form = $(document);
    //console.log(form);
    openTab(region_code);
})

function openTab(_region_id) {
    var i, tablinks;
    /*x = document.getElementsByClassName("content-tab");
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }*/
    tablinks = document.getElementsByClassName("tab");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" is-active", "");
    }
    if (_region_id.length !== 0) {
        document.getElementById(_region_id).className += " is-active";
    } else {
        if (document.getElementById('All')) {
            document.getElementById('All').className += " is-active";
        }
    }
}