/**
 * Created by edgarsavotins on 16/05/17.
 */

$(function(){
    $('.stop-propagation').on('click', function (e) {
        e.stopPropagation();
    });
});

$(function(){
    $('.default-hide').hide();
});

$(document).ready(function() {
    $('.datepicker').datepicker({
        autoclose: true,
        format: 'yyyy-mm-dd',
        startDate: "today",
        maxViewMode: 0,
        language: "lv",
        daysOfWeekHighlighted: "0,6",
        todayHighlight: true
    });
});

$(document).on('click', 'th.datepicker-switch, span.month, td.day, th.next, th.prev, th.switch, span.year', function (e) {
    e.stopPropagation();
});

$(function(){

    $('#komandejums-radio').click(function(){ $('#myform-vieta').show(); $('#myform-iesniegums').hide(); });
    $('#atvalinajums-radio').click(function(){ $('#myform-iesniegums').show(); $('#myform-vieta').hide(); })

});
