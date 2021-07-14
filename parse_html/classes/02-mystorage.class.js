
// ---------------------------------------------------------------
// MyStorage
// ---------------------------------------------------------------

class MyStorage{
    static save(key, value){ // MyStorage.save('data',{})
        localStorage.setItem(key, JSON.stringify(value));
    }

    static get(key){ // MyStorage.get('data')
        return JSON.parse(localStorage.getItem(key)) ;
    }

    static update(key, id, value){ // MyStorage.update('data', 'item', {})
        var ele = MyStorage.get(key);
        ele[id]=value;
        MyStorage.save(key, ele);
    }

    static reset(){ // MyStorage.reset()
        localStorage.clear();
    }
}

