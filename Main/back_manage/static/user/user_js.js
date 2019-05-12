

function add_url_query_user(){
    let a = $('.query-user');
    let query_value = $('#user').val();
    console.log(query_value);
    a.attr(
        'href', '?query=user&user=' + query_value
    )
}