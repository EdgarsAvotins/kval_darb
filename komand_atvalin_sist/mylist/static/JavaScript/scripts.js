/**
 * Created by edgarsavotins on 16/05/17.
 */

$(function(){
    $.validator.addMethod("alpha", function(value, element) {
        return this.optional(element) || value == value.match(/^[a-zA-Z]+$/);
    });
});


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

$( 'body' ).on( 'click', '#enable-upload', function() {
    if( $(this).attr('data-toggle') != 'button' ) { $(this).toggleClass('active');      }
    if( $(this).hasClass( 'active' ) == true )    { $("input").prop('disabled', false); }
    if( $(this).hasClass( 'active' ) == false )   { $("input").prop('disabled', true);  }
});

$(function(){
    $('.enable-upload1').on('click', function () {
        if ($(this).is(':checked')) {$('.ceks-upload1').prop('disabled', false);}
        else {$('.ceks-upload1').prop('disabled', true);}
    });
});

$(function(){
    $('.enable-upload2').on('click', function () {
        if ($(this).is(':checked')) {$('.ceks-upload2').prop('disabled', false);}
        else {$('.ceks-upload2').prop('disabled', true);}
    });
});

$(function(){
    $('#search-input1').on('input', function() {
        var input_value = $(this).val();
        $('.user-full-name1').each (function () {
            if ($(this).text().toLowerCase().indexOf(input_value) >= 0 ) { $(this).show(); }
            else {$(this).hide();}
        })
    });
});

$(function(){
    $('#search-input2').on('input', function() {
        var input_value = $(this).val();
        $('.user-full-name2').each (function () {
            if ($(this).text().toLowerCase().indexOf(input_value) >= 0 ) { $(this).show(); }
            else {$(this).hide();}
        })
    });
});