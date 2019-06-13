var va = $('#id_tableName');

function check_file_one() {
    let va = $('#id_tableUrl');
    let v = va.val();
    let re = new RegExp('^[a-z]*?[_|-]?[a-z]*?(.html)?$');
    let res = re.test(v);
    let va1 = '/' + v;
    if (res){
        va.val(va1);
    }else{
        va.val('/');
    }
}
function check_file() {
    let v = va.val();
    if (v) {
        let re = new RegExp('^[a-z]*?[_|-]?[a-z]*?(.html)?$');
        let res = re.test(v);
        let va1 = '/' + v;
        if (res){
            va.val(va1);
        }else{
             va.val('/');
        }
    }
}
function check_file_two(self) {
    let va = self.value;
    let re = new RegExp('^[a-z]*?[_|-]?[a-z]*?(.html)?$');
    let res = re.test(va);
    if (res){
        self.value = '/' + va;
    }
}

// va.change(function(){
//     let v = $(this).children('option:selected').val();
//     if (v){
//         alert(v);
//         $.ajax({
//             url: '/back_manage/permission/?query=per_query&mid=' + v,
//             type: 'GET',
//             success:function(arg){
//                 alert(arg)
//             }
//         })
//     }
// });