// ---------------------------------------------------------------
// Config
// ---------------------------------------------------------------

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
