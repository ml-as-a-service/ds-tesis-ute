
var config = {
    'cuencas':{
        'is_root': true,

        'ele_id':'ctl00_ContentPlaceHolder1_cboCuenca',
        'ele_id_child':'ctl00_ContentPlaceHolder1_cboSubcuenca',
        'ele_id_parent':'',

        'name': 'cuencas',
        'name_item':'cuenca',
        'name_child': 'subcuencas',
        'name_parent': '',
        
    },
    'subcuencas':{
        'is_root': false,

        'ele_id':'ctl00_ContentPlaceHolder1_cboSubcuenca',
        'ele_id_child':'ctl00_ContentPlaceHolder1_cboEstacion',
        'ele_id_parent':'ctl00_ContentPlaceHolder1_cboCuenca',

        'name': 'subcuencas',
        'name_item':'subcuenca',
        'name_child': 'estaciones',
        'name_parent': 'cuencas',
        
    },
    'estaciones':{
        'is_root': false,

        'ele_id':'ctl00_ContentPlaceHolder1_cboEstacion',
        'ele_id_child':'ctl00_ContentPlaceHolder1_cboPasos',
        'ele_id_parent':'ctl00_ContentPlaceHolder1_cboSubcuenca',

        'name': 'estaciones',
        'name_item':'estacion',
        'name_child': 'pasos',
        'name_parent': 'subcuencas',
        
    },
    'pasos':{
        'is_root': false,

        'ele_id':'ctl00_ContentPlaceHolder1_cboPasos',
        'ele_id_child':'',
        'ele_id_parent':'ctl00_ContentPlaceHolder1_cboEstacion',

        'name': 'pasos',
        'name_item':'paso',
        'name_child': '',
        'name_parent': 'estaciones',
        
    },
};

class Config{
    static data;        // configuracion 
    static root;        // first element
    static leaf;        // last element
    static steps;   // sequency

    static init(config){
        Config.data = config;
        Config.process();
    }    

    static process(){
        Config.steps = [];
        for (const [key, ele] of Object.entries(Config.data)) {
            if(ele['is_root']){ Config.root = ele }
            if(!ele['ele_id_child']){ Config.leaf = ele }
            Config.steps.push(key);
        }           
    }

    static get(type,key){ // Config.get('subcuencas', 'ele_id');
        if(type=='root' || type=='leaf'){
            return Config[type][key];
        }

        return Config.data[type][key];
    }

    static isRoot(type){ // Config.isRoot('subcuencas')
        return Config.root == Config.data[type];
    }
    static isLeaf(type){ // Config.isLeaf('subcuencas')
        return Config.leaf == Config.data[type];
    }

    static getChild(type){ // Config.getChild('subcuencas')
        var name_child = Config.data[type]['name_child']
        return Config.data[name_child];
    }
    static getParent(type){ // Config.getParent('subcuencas')
        var name_parent = Config.data[type]['name_parent']
        return Config.data[name_parent];
    } 
}

/*
Config.init(config);

console.log('Config.data', Config.data);
console.log('Config.getChild subcuencas', Config.getChild('subcuencas'));
console.log('Config.getParent subcuencas', Config.getParent('subcuencas'));
console.log('Config.isRoot subcuencas', Config.isRoot('subcuencas'));
console.log('Config.isLeaf subcuencas', Config.isLeaf('subcuencas'));
console.log('Config.isRoot cuencas', Config.isRoot('cuencas'));
console.log('Config.isLeaf pasos', Config.isLeaf('pasos'));
console.log('Config.steps', Config.steps);
console.log('Config.get(subcuencas, ele_id)', Config.get('subcuencas', 'ele_id'));
*/


class MyStorage{
    static save(key, value){
        localStorage.setItem(key,JSON.stringify(value));
    }

    static get(key){
        return JSON.parse(localStorage.getItem(key)) ;
    }

    static update(key, id, value){
        var ele = MyStorage.get(key);
        ele[id]=value;
        MyStorage.save(key, ele);
    }

    static reset(){
        localStorage.clear();
    }
}

// -----------------------------------------------

class HtmlCollection{
    static init(type){                                  // HtmlCollection.init('cuencas');
        var collection = new HtmlCollection(type);      // HtmlCollection('cuencas');
        collection.initItems();                         // Creo el "item" y lo anexo al "items"
        return collection;        
    }

    constructor(type){
        this.name = type;                               // cuencas
        this.items = [];
    }

    initItems(){  
        var _this = this;
        var options = System.getOptions(this.name);  // System.getOptions('cuencas')

        for (const [key, value] of Object.entries(options)) {
            var metadata = {
                'id':      key,                    // html option value
                'name':    value,                  // html option text
                'type':    Config.get(_this.name,'name_item'),             // cuencas
                'type_collection':    Config.get(_this.name,'name'),             // cuencas
            };
           
            _this.items.push(HtmlItem.init(metadata));
        }
    }

    export(){
        var items = {};
        this.items.forEach(element => {
            var item = element.export();
            items[item['id']] = item;
        });

        var ret={}; ret[this.name] = items;
        return ret;
    }
}

class HtmlItem{
    static init(metadata){ // HtmlItem.init(metadata);
        var item = new HtmlItem(metadata);
        if(System.isSelected(metadata['type_collection'],metadata['id'])){ // cuencas , GTERRA
            item.initCollection();
        }
        return item;
    }

    constructor(metadata){
        this.id = metadata['id'];                                   // html option value
        this.name = metadata['name'];                               // html option text
        this.type = metadata['type'];                               // cuenca        
        this.type_collection = metadata['type_collection'];         // cuencas        
        this.collection = null;
    }

    initCollection(){
        var collection = null;
        if(!Config.isLeaf(this.type_collection)){ // cuencas
            collection = HtmlCollection.init(Config.get(this.type_collection,'name_child'));
        }
        this.collection = collection;
    }

    export(){
        var ret={
            'id':       this.id,    // html option value
            'name':     this.name,  // html option text
            '_type':    this.type   // cuenca         
        };
        
        if(this.collection){
            for (const [key, value] of Object.entries(this.collection.export())) {
                ret[key] = value;
            }
        }

        return ret;
    }      
}

// -----------------------------------------------
class System{
    static data;
    static selected;

    static init(config){
        Config.init(config);
        System.process();
    }

    static reset(){
        MyStorage.reset();
        MyStorage.save('System.init',true);
        System.process();
        System.backup();
        System.isComplete();
    }
    static next(){        
        var step = System.moveNextStep();   // Me muevo al prox filtro, sino paso a rellenar 
        if(!step){
            // debugger;
            System.process();       // cargo el estado actual
            System.syncronize();    // guardo anexo a memoria el estado actual
            System.isComplete();
            System.moveNextStep();   
        }
    }

    static process(){
        System.data = null;
        System.data = HtmlCollection.init(Config.get('root','name')); // cuencas        
    }

    static getEle(type){ // System.getEle('cuencas');
        return jQuery('#'+Config.get(type,'ele_id'));
    }    
    static getOptions(type){ // System.getOptions('cuencas');
        var options = {};
        jQuery("option", System.getEle(type)).each(function() {
            options[this.value] = this.text;
        });
        return options;          
    }   
    static getSelectedOptions(){ // System.getSelectedOptions();
        System.selected = {};
        for (const [key, value] of Object.entries(Config.data)) {
            System.selected[key] = jQuery("option:selected", System.getEle(key)).val();
        }  
        return System.selected;
    }

    static isSelected(type, ele_key){ // System.isSelected('cuencas','GTERRA');
        System.getSelectedOptions();
        return System.selected[type] == ele_key; 
    }

    static getSelectedData(){
        // debugger;
        var data = System.data.export(); // dataset 
        var current = data;
        for (const [idx, type] of Object.entries( Config.steps )) {  
            if(!Config.isLeaf(type)){
                var ds = current[type]; // current['cuencas']
                var key_selected;
                for (const [key, value] of Object.entries(ds)) {
                    if(!System.isSelected(type,key)){
                        delete(ds[key]);
                    }else{
                        key_selected = key;
                    }
                }
                current = ds[key_selected];
            }
        }
        return data;
    }

    static resetNextSteps(){
        System.nextSteps = {
            'cuenca':null, 
            'subcuenca':null, 
            'estacion':null, 
            'paso':null};
        MyStorage.save('nextSteps',System.nextSteps);        
    }
    static saveNextStep(id, type){
        MyStorage.save('nextStep',{
            'id': id,
            'type': type,
        });
        // a los siguientes del nivel eliminarlos
        var cleanItem = false;
        for (const [idx, ele] of Object.entries( Config.steps )) {
            var name_item = Config.get(ele,'name_item'); // 
            if(cleanItem){
                System.updateNextSteps(name_item,'');
            }
            if(name_item == type){
                cleanItem = true;
            }
        }
    }
    static updateNextSteps(id, type){ // BARD, cuenca
        MyStorage.update('nextSteps',id, type);       
    } 

    static isComplete(data, level){ // dataset, 
        // debugger;
        if(!level){
            level = Config.get('root','name');
            var data =  System.recovery(); //System.data.export(); 

            data = data[level]; // data['cuencas']
            System.breakIsComplete = false;
        }

        for (const [key, ele] of Object.entries(data)) { // BARD . {}
            if(System.breakIsComplete) return false;

            var type = ele['_type'];
            
            if(Config.isLeaf(level)){System.updateNextSteps(type, key); return true;} // last level  pasos
            if(Config.isRoot(level)) System.resetNextSteps(); // first level cuencas
            
            System.updateNextSteps(type, key); // cuenca BARD

            var sublevel = Config.get(level,'name_child');
            if(typeof ele[sublevel] == 'undefined'){
                // debugger
                System.saveNextStep(key, type);
                System.breakIsComplete = true;
                return false;
            }else{
                System.isComplete(ele[sublevel], sublevel);
            }
        }
    }

    static moveNextStep(){
        var nextSteps = MyStorage.get('nextSteps'); 
        for (const [idx, ele] of Object.entries( Config.steps )) {  // 0 cuencas
            var name_item = Config.get(ele,'name_item'); // cuenca
            var combo_id = nextSteps[name_item]; // CYENS
            if(System.isSelected(ele,combo_id)){ // cuencas , GTERRA
                System.updateNextSteps(name_item,'');
            }else if(combo_id){
                var ele_id = Config.get(ele,'ele_id');
                // debugger;
                System.updateNextSteps(name_item,'');
                System.getEle(ele).val(combo_id).change();
                return combo_id;
                break;
            }
        }
        return false;
    }
    static backup(){
        var data = System.data.export();
        MyStorage.save('data',data);
        MyStorage.save('selected',System.selected);

        // var url = "https://ml-as-a-service.com/tesis/save.php";
        // jQuery.post( url, {'data': data}, function( res ) {
        //     console.log('ajax backup', res);
        // });

    }

    static recovery(){
        return MyStorage.get('data');
    }

    static syncronize(){
        // var data_selected = System.getSelectedData();
        var data_selected = System.data.export();
        var data_recovery = System.recovery();

        var target ={};
        jQuery.extend( true, target, data_recovery, data_selected );
        console.log(target);
        
        MyStorage.save('data',target);
        MyStorage.save('selected',System.selected);
    }

    static check(){
        var selected = System.getSelectedOptions();
        var data = System.recovery();

        var current = data;
        for (const [idx, type] of Object.entries( Config.steps )) {  
            current = current[type][selected[type]];
        } 
        console.log('existe', selected, 'en el localstorage');
    }
}


// ------------------------------------------------------------
var s = document.createElement("script"); 
s.src = "https://code.jquery.com/jquery-3.6.0.min.js"; 
s.onload = function(e){ 
    // debugger;
    console.log('build_hierarchical');
    System.init(config);

    // console.log('Config.steps', Config.steps);
    // console.log('System.getOptions(cuencas)', System.getOptions('cuencas'));
    // console.log('System.getSelectedOptions()', System.getSelectedOptions());
    // console.log('Config.get(root,name)', Config.get('root','name'));
    // console.log('System.data', System.data);
    
    System.process();
    // console.log('System.data.export()',System.data.export())
    // console.log('System.getSelectedData()',System.getSelectedData())

    // System.backup();
    // System.isComplete();

    // console.log('Config.root', Config.root);
    // System.initHtmlHierarchy();
    // console.log('System.data', System.data);
    mgrun();
};  
document.head.appendChild(s);  



/*

function mgrun(){
    var option = 3;
//debugger;
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
    console.log('cargo https://ml-as-a-service.com/tesis/build_hierarchical.js');
};  
document.head.appendChild(s);  

*/

