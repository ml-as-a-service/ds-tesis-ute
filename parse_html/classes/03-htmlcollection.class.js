
// ---------------------------------------------------------------
// HtmlCollection
// ---------------------------------------------------------------

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

