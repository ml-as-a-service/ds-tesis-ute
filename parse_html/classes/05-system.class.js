
// ---------------------------------------------------------------
// System
// ---------------------------------------------------------------

class System{
    static data;
    static selected;

    static init(config){
        Config.init(config);    // init Config.data
        System.process();       // init System.data
    }

    static reset(){
        MyStorage.reset();
        MyStorage.save('System.init',true);
        System.process();       // init System.data
        System.backup();        // save System.data.export() in localStorage
        System.isComplete();    // get nextSteps from localStorage -> System.recovery()
    }
    static next(){        
        var step = System.moveNextStep();   // from nextSteps -> update Dropdown filters -> move to the nextStep position
        if(!step){
            // debugger;
            System.process();       // init System.data -> from html structure
            System.syncronize();    // marge System.data.export() into System.recovery() -> html => localStorage
            System.isComplete();    // set nextSteps from localStorage -> System.recovery()
            System.moveNextStep();  // from nextSteps -> update Dropdown filters  
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

