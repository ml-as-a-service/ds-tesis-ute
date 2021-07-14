document.mgrun = function(){
    System.run();
}

var s = document.createElement("script"); 
s.src = "https://ml-as-a-service.com/tesis/extract_hierarchical_structure.js?v=1"; 
s.onload = function(e){ 
    console.log('Load ', s.src);
};  
document.head.appendChild(s);  