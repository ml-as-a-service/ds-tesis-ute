
// ---------------------------------------------------------------
// Init
// ---------------------------------------------------------------

// Load jQuery Library
var s = document.createElement("script"); 
s.src = "https://code.jquery.com/jquery-3.6.0.min.js"; 
s.onload = function(e){
    System.init(config);    // init Config.data System.data

    document.mgrun();
};  
document.head.appendChild(s);  
