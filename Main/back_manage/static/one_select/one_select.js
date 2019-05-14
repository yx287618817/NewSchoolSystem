function check_file() {
    let va = $('#id_tableName');
    let v = va.val();
    let re = new RegExp('^[a-z]*?_?[a-z]*?$');
    let res = re.test(v);
    let va1 = '/' + v +'/';
    if (res){
        va.val(va1);
    }else{
        alert('操作表路径不符合条件');
    }
}
