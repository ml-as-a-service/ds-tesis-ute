
// ---------------------------------------------------------------
// Init
// ---------------------------------------------------------------

// Load jQuery Library
var s = document.createElement("script"); 
s.src = "https://code.jquery.com/jquery-3.6.0.min.js"; 
s.onload = function(e){
    System.init(config);    
    System.process();
    document.mgrun();
};  
document.head.appendChild(s);  
