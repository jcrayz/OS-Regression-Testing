/**
 * Activates the pill in the navigation bar based on the URL
 */
function setActiveTab() {
    var page = window.location.pathname;
    var logs_pill = "logs_pill";
    var home_pill = "home_pill";

    // if url=/logs, set element logs_pill class to "active"
    if (page == "/logs") {
        document.getElementById(logs_pill).classList.add('active');
        document.getElementById(home_pill).classList.remove('active');
    } else {
        document.getElementById(home_pill).classList.add('active');
        document.getElementById(logs_pill).classList.remove('active');
    }
}

/**
 * Finds all elements classed as "pass_row" and alternately hides and displays them
 */
function togglePassingTests() {
    var passing_rows = document.getElementsByClassName("tr-pass");
    var toggle_btn = document.getElementById("toggle-pass");
    var hide_msg = "Hide Passing Tests";
    var show_msg = "Show Passing Tests";
    if (toggle_btn.innerHTML == hide_msg) {
        toggle_btn.innerHTML = show_msg;
    } else {
        toggle_btn.innerHTML = hide_msg;
    }
    for (var i = 0; i < passing_rows.length; i++) {
        if (passing_rows[i].style.display == "none") {
            passing_rows[i].style.display = "table-row";
        } else {
            passing_rows[i].style.display = "none";
        }
    }
}