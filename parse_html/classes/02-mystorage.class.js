
// ---------------------------------------------------------------
// MyStorage
// ---------------------------------------------------------------

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

