/**
 * Created by edgarsavotins on 16/05/17.
 */

// ja uzspiez, apstadinat logu aizversanu (dropdown, popup utt)
$(function(){
    $('.stop-propagation').on('click', function (e) {
        e.stopPropagation();
    });
});

// paslept uzreiz visus elementus ar so klasi
$(function(){
    $('.default-hide').hide();
});

// pirma datuma izveles loga iestatijumi
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

// otra datuma izveles loga iestatijumi
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

// ja nospiez datuma izvelne uz jebkuru pogu, apstadinat jebka aizversanu (šajā gadījumā, dropdown, kurā atrodas šis datepicker)
$(document).on('click', 'th.datepicker-switch, span.month, td.day, th.next, th.prev, th.switch, span.year', function (e) {
    e.stopPropagation();
});

// ja nospiez atvalinajumu, paradit tikai iesnieguma iesutisanu, ja komandejumu, tad vietu
// padarit redzamos laukus obligatus
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

// atkariba no atķeksēšanas, padarīt čeku iesūtīšanu pieejamu un obligātu vai otrādāk, ja neatķeksē
// šis atbilst par "pievienot atskaiti" popup
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

// atkariba no atķeksēšanas, padarīt čeku iesūtīšanu pieejamu un obligātu vai otrādāk, ja neatķeksē
// šis atbilst par "labot atskaiti" popup
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

// ja vards, kurus ieraksta mekletaja, neietilpst kada no lietotaju vardiem, tad paslept lietotaju
// ja ietilpst, paradit
$(function(){
    $('#search-input1').on('input', function() {
        var input_value = $(this).val();
        $('.user-full-name1').each (function () {
            if ($(this).text().toLowerCase().indexOf(input_value.toString().toLowerCase()) >= 0 ) { $(this).show(); }
            else {$(this).hide();}
        })
    });
});

// ja vards, kurus ieraksta mekletaja, neietilpst kada no lietotaju vardiem, tad paslept lietotaju
// ja ietilpst, paradit
$(function(){
    $('#search-input2').on('input', function() {
        var input_value = $(this).val();
        $('.user-full-name2').each (function () {
            if ($(this).text().toLowerCase().indexOf(input_value.toString().toLowerCase()) >= 0 ) { $(this).show(); }
            else {$(this).hide();}
        })
    });
});

// ja vards, kurus ieraksta mekletaja, neietilpst kada no lietotaju vardiem, tad paslept lietotaju
// ja ietilpst, paradit
$(function(){
    $('#search-input').on('input', function() {
        var input_value = $(this).val();
        $('.user-full-name').each (function () {
            if ($(this).val().toLowerCase().indexOf(input_value.toString().toLowerCase()) >= 0 ) { $(this).show(); }
            else {$(this).hide();}
        })
    });
});

// ja tabula tukša, tad atspējot visas pogas
$(function(){
    if (!$('td:nth-child(1)').text().length) {
        $('.filter-status').prop('disabled', true);
        $('.filter-vacation').prop('disabled', true);
        $('.filter-business-trip').prop('disabled', true);
        $('.filter-all').prop('disabled', true);
    }
});

// ja uzspiež uz pogu "komandejumi", paradit tikai komandejumus un atspējot pogu
$(function(){
    $('.filter-business-trip').on('click', function () {
        $('.row-vacation').hide();
        $('.row-business-travel').show();
        $(this).prop('disabled', true);
        $('.filter-vacation').prop('disabled', false);
        $('.filter-all').prop('disabled', false);
    });
});

// ja uzspiež uz pogu "atvalinajumi", paradit tikai atvalinajumus un atspējot pogu
$(function(){
    $('.filter-vacation').on('click', function () {
        $('.row-vacation').show();
        $('.row-business-travel').hide();
        $(this).prop('disabled', true);
        $('.filter-business-trip').prop('disabled', false);
        $('.filter-all').prop('disabled', false);
    });
});

// ja nospiež pogu "visi", tad rādīt gan atvaļinājumus, gan komandējumus un atspējot šo pogu
$(function(){
    $('.filter-all').on('click', function () {
        $('.row-vacation').show();
        $('.row-business-travel').show();
        $(this).prop('disabled', true);
        $('.filter-vacation').prop('disabled', false);
        $('.filter-business-trip').prop('disabled', false);
    });
});

// ja nospiež pogu "kartiba", tad parādīt/paslēpt ierakstus ar statusu "kārtībā"
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

//ja uzspiež krustiņu, tad to vārdu paslēpj un nomaina value uz 1, tādā veidā pasakot backend, ka tas jādzēš
$(function(){
    $('.delete-user-from-saved').on('click', function () {
        var button = $(this);
        button.find('input').prop('value', 1);
        button.parent().hide();
        $('.save-user-changes-btn').prop('disabled', false);
    });
});

// ja ir iziets ārā un ieiets atpakaļ, "reset", jeb parādīt paslēptos lietotājus un noņemt value, lai pa jaunam dzēstu
$(function(){
    $('.saved-users').on('click', function () {
        $('.saved-users-full-name').each (function () {
            $(this).show();
            $(this).find('input').prop('value', null);
        });
        $('.save-user-changes-btn').prop('disabled', true);
    });
});