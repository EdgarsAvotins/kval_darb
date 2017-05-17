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

// $(document).ready(function () {
//
//     var date_input1=$('input[name="datums_no"]');
//     var container1=$('.bootstrap-iso form').length>0 ? $('.bootstrap-iso form').parent() : "body";
//     var options1={
//     format: 'yyyy-mm-dd',
//     container: container1,
//     startDate: "today",
//     maxViewMode: 0,
//     language: "lv",
//     daysOfWeekHighlighted: "0,6",
//     todayHighlight: true,
//     autoclose: true
//     };
//     date_input1.datepicker(options1);
//
//     var date_input2=$('input[name="datums_lidz"]');
//     var container2=$('.bootstrap-iso form').length>0 ? $('.bootstrap-iso form').parent() : "body";
//     var options2={
//     format: 'yyyy-mm-dd',
//     container: container2,
//     startDate: "today",
//     maxViewMode: 0,
//     language: "lv",
//     daysOfWeekHighlighted: "0,6",
//     todayHighlight: true,
//     autoclose: true
//     };
//     date_input2.datepicker(options2);
//
//     $(document).on('click', 'th.datepicker-switch, span.month, td.day, th.next, th.prev, th.switch, span.year', function (e) {
//         e.stopPropagation();
//     });
// });

$(function(){

    $('#komandejums-radio').click(function(){ $('#myform-vieta').show(); $('#myform-iesniegums').hide(); });
    $('#atvalinajums-radio').click(function(){ $('#myform-iesniegums').show(); $('#myform-vieta').hide(); })

});
