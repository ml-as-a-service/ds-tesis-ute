

// ---------------------------------------------------------------
// Config
// ---------------------------------------------------------------

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
