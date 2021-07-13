document.mgrun = function(){
    var option = 0;

    switch(option) {
    case 1:
        System.reset();
        break;
    case 2:
        System.next();
        break;
    case 3:
        System.check();
        break;
    default:
        // code block
    }
}

var s = document.createElement("script"); 
s.src = "https://ml-as-a-service.com/tesis/build_hierarchical.js?v=13"; 
s.onload = function(e){ 
    console.log('Load ', s.src);
};  
document.head.appendChild(s);  