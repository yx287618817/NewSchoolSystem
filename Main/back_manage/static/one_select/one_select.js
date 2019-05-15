function check_file_one() {
    let va = $('#id_tableUrl');
    let v = va.val();
    let re = new RegExp('^[a-z]*?_?[a-z]*?$');
    let res = re.test(v);
    let va1 = v +'/';
    if (res){
        va.val(va1);
    }else{
        va.val('/');
    }
}

function check_file() {
    let va = $('#id_tableName');
    let v = va.val();
    if (v) {
        let re = new RegExp('^[a-z]*?_?[a-z]*?$');
        let res = re.test(v);
        let va1 = '/' + v;
        if (res){
            va.val(va1);
        }else{
             va.val('/');
        }
    }
}