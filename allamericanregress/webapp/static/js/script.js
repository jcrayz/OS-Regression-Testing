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