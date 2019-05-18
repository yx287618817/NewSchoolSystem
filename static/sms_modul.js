// 用户填写验证码后进行验证
  function verification_code() {
      let code = $('.sms_code').val(); //获取上传的文件
      // console.log(code);
      // console.log(code.length);
      if (code) {
        let data = new FormData();
        data.append('code', code);
        $.ajax({
            url: '/sms_verification/',
            type: 'POST',
            data: data,
            processData: false,
            contentType: false,
        }).done(function(arg) {
          if (arg=='false'){
              alert('验证码不正确')
        }else{
              // 忘记密码界面,验证码正确继续步骤
              $('.result-div').css(
                  'display','inline'
              );
              // 注册界面继续注册
              $('.result-result').attr(
                  'disabled', false
              )
          }
        })}}

// 点击按钮发送验证码, 发送成功则按钮不能再次按下
function send_verification_code() {
  let tel = $('#id_student_tel').val(); //手机号码
  let re = new RegExp('^((13[0-9])|(14[5,7,9])|(15[^4])|(18[0-9])|(17[0,1,3,5,6,7,8]))\\d{8}$');
  let tel_res = re.test(tel);
  if (tel_res) {
    let data = new FormData();
    data.append('tel', tel);
    $.ajax({
        url: '/sms_verification/',
        type: 'POST',
        data: data,
        processData: false,
        contentType: false,
    }).done(function(arg) {
        let send_code = $('.sms_code_verification');
        send_code.val(arg);
        if (arg=='发送成功'){
            send_code.attr(
                'disabled', true
            )}
    })
  }else{
      alert('手机号码不正确...')
  }
}

// 验证密码是否符合规范
  function verification_pwd() {
      let pwd_input = $('#new-pwd');
      let pwd = pwd_input.val();
      let re = new RegExp('^[A-Za-z][A-Za-z0-9]{7,23}');
      let result = re.test(pwd);
      if (result){
          $('.result').attr(
              'disabled', false
          );
           pwd_input.css(
              'color', 'black'
          );
      }else {
          $('.result').attr(
              'disabled', true,
          );
           pwd_input.css(
              'color', 'red'
          );
      }
  }


// 验证账号是否存在
  function verification_username_have() {
      let username = $('#username').val();
      let data = {
          'username': username,
          'verification_str': 'verification_username'
      };
      $.ajax({
          url: '/forget_passwd/',
          type:'GET',
          data: data,
          success:function (arg) {
              let obj = JSON.parse(arg);
              let res = JSON.parse(obj.verification_username_result);
              if (!res){
                  alert('用户名不存在')
              }
          }
      })
  }