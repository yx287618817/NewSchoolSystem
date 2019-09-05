$.ajaxSetup({
         data: {csrfmiddlewaretoken: '{{ csrf_token }}' },
     });
function delete_select(self) {
    console.log(self.value);
    $.ajax({
        url: '/register_two/',
        type: 'POST',
        data: {
            'delete': self.value
        },
        success: function (arg) {
            if (arg == 'ok'){
                self.remove()
            }
        }
    })
}
function majorSelect(self) {
     let major_s = self.options[self.selectedIndex].value + ',' +
     self.options[self.selectedIndex].text;
    $.ajax({
        url: '/register_two/',
        type: 'POST',
        data: {
            'p': major_s,
        },
        success: function (arg) {
            if (arg == 'error') {
                alert('专业选择不能超过10个，请谨慎选择！');
            }else if(arg == 'false'){
                alert('未知错误');
            }else if(arg == 'update_error'){
                alert('请勿重复添加');
            }else{
                let a = eval(arg);
                console.log(a);
                let but = document.createElement('button');
                let di = document.createElement('div');
                di.setAttribute('class', 'col-md-12');
                but.setAttribute("class", "btn center-block major-selected");
                but.setAttribute("value", a[0]);
                but.setAttribute( "onclick", "delete_select(this)");
                but.innerText = a[1];
                di.append(but);
                $('.major-new').append(di);
        }}
        })}