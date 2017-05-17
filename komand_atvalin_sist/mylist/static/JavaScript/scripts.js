/**
 * Created by edgarsavotins on 16/05/17.
 */

$(document).ready(function () {
    $('.stop-propagation').on('click', function (e) {
        e.stopPropagation();
    });

    $(function () {
        var date_input=$('input[name="datums_no"]');
        var container=$('.bootstrap-iso form').length>0 ? $('.bootstrap-iso form').parent() : "body";
        var options={
        format: 'yyyy-mm-dd',
        container: container,
        startDate: "today",
        maxViewMode: 0,
        language: "lv",
        daysOfWeekHighlighted: "0,6",
        todayHighlight: true,
        autoclose: true,
        };
        date_input.datepicker(options);
    });

    $(function () {
        var date_input=$('input[name="datums_lidz"]');
        var container=$('.bootstrap-iso form').length>0 ? $('.bootstrap-iso form').parent() : "body";
        var options={
        format: 'yyyy-mm-dd',
        container: container,
        startDate: "today",
        maxViewMode: 0,
        language: "lv",
        daysOfWeekHighlighted: "0,6",
        todayHighlight: true,
        autoclose: true,
        };
        date_input.datepicker(options);
    });

    $(document).on('click', 'th.datepicker-switch, span.month, td.day, th.next, th.prev, th.switch, span.year', function (e) {
        e.stopPropagation();
    });
});

$(function(){

    $('#komandejums-radio').click(function(){ $('#myform-vieta').show(); $('#myform-iesniegums').hide(); });
    $('#atvalinajums-radio').click(function(){ $('#myform-iesniegums').show(); $('#myform-vieta').hide(); })

});
