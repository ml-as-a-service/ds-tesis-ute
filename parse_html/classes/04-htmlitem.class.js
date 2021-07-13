
// ---------------------------------------------------------------
// HtmlItem
// ---------------------------------------------------------------

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

