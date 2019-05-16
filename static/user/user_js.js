function add_url_query_user() {
        let a = $('.query-user');
        let user = $('#user').val();
        a.attr(
            'href', '?query=user&user=' + user
        )
    }

    function select_group() {
        let s_id = $('#select_group').val();
        let user = $('#user').val();
        $('.select_id_update').attr(
            'href', '?query=update_user&user=' + user + '&s_id=' + s_id,
        );
        $('.select_id_add').attr(
            'href', '?query=add_user&user=' + user + '&s_id=' + s_id,
        );
    }