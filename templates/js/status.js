
/*This making panels inner hideable by clicking on theirs header */
$('.panel-hm').each(function(index) {
    mm = $(this).children('.panel-heading').find('.minmax');
    mm.click(function() {
        pb = $(this).parent().parent().siblings('.panel-body')[0];
        if($(pb).is(':hidden')) {
            $(pb).slideDown();
            $(this).text("-");
        } else {
            $(pb).slideUp();
            $(this).text("+");
        }
    });
});


$("#first_col, #second_col, #third_col").sortable({
    connectWith: '.sortconn',
    handle: '.move'
}).disableSelection();

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