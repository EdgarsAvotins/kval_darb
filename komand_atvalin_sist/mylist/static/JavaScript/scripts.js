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
    $('.datepicker1').datepicker({
        autoclose: true,
        format: 'yyyy-mm-dd',
        startDate: "today",
        maxViewMode: 0,
        language: "lv",
        daysOfWeekHighlighted: "0,6",
        todayHighlight: true
    });
});

$(document).ready(function() {
    $('.datepicker2').datepicker({
        autoclose: true,
        format: 'yyyy-mm-dd',
        startDate: "today",
        maxViewMode: 0,
        language: "lv",
        daysOfWeekHighlighted: "0,6",
        todayHighlight: true
    });
});

// $(document).ready(function() {
//     $('.datepicker2').datepicker('setDates', [new Date(2017, 11, 11)]);
// });

$(document).on('click', 'th.datepicker-switch, span.month, td.day, th.next, th.prev, th.switch, span.year', function (e) {
    e.stopPropagation();
});

$(function(){

    $('#komandejums-radio').click(function(){
        $('#myform-vieta').show();
        $('#myform-iesniegums').hide();
        $('#jauns-ieraksts-iesniegums').prop('required', false);
        $('#input-vieta').prop('required', true); });

    $('#atvalinajums-radio').click(function(){
        $('#myform-iesniegums').show();
        $('#myform-vieta').hide();
        $('#jauns-ieraksts-iesniegums').prop('required', true);
        $('#input-vieta').prop('required', false); })

});

// $( 'body' ).on( 'click', '#enable-upload', function() {
//     if( $(this).attr('data-toggle') != 'button' ) { $(this).toggleClass('active');      }
//     if( $(this).hasClass( 'active' ) == true )    { $("input").prop('disabled', false); }
//     if( $(this).hasClass( 'active' ) == false )   { $("input").prop('disabled', true);  }
// });

$(function(){
    $('.enable-upload1').on('click', function () {
        if ($(this).is(':checked')) {
            $('.ceks-upload1').prop('disabled', false);
            $('.ceks-upload1').prop('required', true);
        }
        else {
            $('.ceks-upload1').prop('disabled', true);
            $('.ceks-upload1').prop('required', false);
        }
    });
});

$(function(){
    $('.enable-upload2').on('click', function () {
        if ($(this).is(':checked')) {
            $('.ceks-upload2').prop('disabled', false);
            $('.ceks-upload2').prop('required', true);
        }
        else {
            $('.ceks-upload2').prop('disabled', true);
            $('.ceks-upload2').prop('required', false);
        }
    });
});

$(function(){
    $('#search-input1').on('input', function() {
        var input_value = $(this).val();
        $('.user-full-name1').each (function () {
            if ($(this).text().toLowerCase().indexOf(input_value.toString().toLowerCase()) >= 0 ) { $(this).show(); }
            else {$(this).hide();}
        })
    });
});

$(function(){
    $('#search-input2').on('input', function() {
        var input_value = $(this).val();
        $('.user-full-name2').each (function () {
            if ($(this).text().toLowerCase().indexOf(input_value.toString().toLowerCase()) >= 0 ) { $(this).show(); }
            else {$(this).hide();}
        })
    });
});

$(function(){
    $('#search-input').on('input', function() {
        var input_value = $(this).val();
        $('.user-full-name').each (function () {
            if ($(this).val().toLowerCase().indexOf(input_value.toString().toLowerCase()) >= 0 ) { $(this).show(); }
            else {$(this).hide();}
        })
    });
});

$(function(){
    if (!$('td:nth-child(1)').text().length) {
        $('.filter-status').prop('disabled', true);
        $('.filter-vacation').prop('disabled', true);
        $('.filter-business-trip').prop('disabled', true);
        $('.filter-all').prop('disabled', true);
    }
});

$(function(){
    $('.filter-business-trip').on('click', function () {
        $('.row-vacation').hide();
        $('.row-business-travel').show();
        $(this).prop('disabled', true);
        $('.filter-vacation').prop('disabled', false);
        $('.filter-all').prop('disabled', false);
    });
});

$(function(){
    $('.filter-vacation').on('click', function () {
        $('.row-vacation').show();
        $('.row-business-travel').hide();
        $(this).prop('disabled', true);
        $('.filter-business-trip').prop('disabled', false);
        $('.filter-all').prop('disabled', false);
    });
});

$(function(){
    $('.filter-all').on('click', function () {
        $('.row-vacation').show();
        $('.row-business-travel').show();
        $(this).prop('disabled', true);
        $('.filter-vacation').prop('disabled', false);
        $('.filter-business-trip').prop('disabled', false);
    });
});

$(function(){
    $('.filter-status').on('click', function () {
        if ($(this).hasClass('filter-active')) {
            $(this).toggleClass('filter-active');
            $('.row-good-status').prop('hidden', false);
        }
        else {
            $(this).toggleClass('filter-active');
            $('.row-good-status').prop('hidden', true);
        }
    });
});