function query_permission() {
      let gid = $('#group_select').val();
      let a = $('.get_permission_a');
     a.attr(
         'href', '?query=group&gid=' + gid,
     );
     document.getElementsByClassName('get_permission_a')[0].click();
  }
