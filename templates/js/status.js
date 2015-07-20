
/*This making panels inner hideable by clicking on theirs header */
$('.panel-hm').each(function(index) {
    $(this).children('.panel-heading').click(function() {
        pb = $(this).siblings('.panel-body')[0] /*gets object of current panel body*/
        if($(pb).is(':hidden')) {
            $(pb).slideDown()
        } else {
            $(pb).slideUp()
        }
    });
});

/* Iteration over each group element and periodic receiving theirs data using AJAX */
$('.table-hm').each(function(index, element) {
    $(element).everyTime('5s',function() {
        group_id = $(element).attr('group')
        $.post('index', {'group': group_id}).done(function(data){
            $(element).children('tbody').html(data)
        });
    });
});

$('.panel-hm').each(function() {
    index = $(this).attr('col')
    $(this).appendTo('#'+index)
});