function query_permission() {
      let gid = $('#group_select').val();
     $('.get_permission_a').attr(
         'href', '?query=group&gid=' + gid,
     )
  }
