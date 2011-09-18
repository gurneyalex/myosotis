CubicWeb.require('ajax.js');

function cancelSelectedMergePersonne(eid) {
    //console.log('cancel merge');
    var holder = jQuery('#personnemergeformholder' + eid);
    $('#acmergepersonne').val('');
    holder.children("div#personne_entities_holder").empty();
    toggleVisibility("sgformbuttons");
}

function mergePersonnes(eid) {
    //console.log('do merge');
    var $input = $('#personnemergeformholder' + eid + ' input')[0];
    var otherEid = $('input[name=selected-personne]').attr('value');
    var name = $('#acmergepersonne').val().strip(',');
    //console.log("call merge personnes ", eid, otherEid);
    var d = asyncRemoteExec('merge_personnes', eid, otherEid);
    d.addCallback(
        function() {
            window.open('\/'+eid, '_self');
   });

}

function personneToMergeSelector(eid) {
  //console.log('personne to merge selector');
  var $holder = $('#personnemergeformholder' + eid);
  var name = $('#acmergepersonne').val().strip(',');
  var entities = asyncRemoteExec("personne_entity_html", eid, name);
  entities.addCallback(function  (entitieslist) {
    //log(entitieslist);
    var dom = getDomFromResponse(entitieslist);
    $('#personne_entities_holder').empty().append(dom);
    if( $("#personne_entities_holder").find('div#personneEntities').length ) {
        $('#sgformbuttons').show();}
    else{
      $('#sgformbuttons').hide();
    }
    });
  $('#acmergepersonne').focus();
};

function initMergePersonnes(){
  //console.log('initMergePersonnes');
  var $input = $('#acmergepersonne');
  var personneeid = $('#personneeid').val();
  //console.log('personne eid ', personneeid );
  //console.log($input.length);
  $input.keypress(function (event) {
    //console.log($input.val());
    if (event.keyCode == KEYS.KEY_ENTER) {
      if ($input.val()){
        if ($('#sgformbuttons').hasClass('hidden')){
          toggleVisibility('sgformbuttons');
        }
        personneToMergeSelector(personneeid);
      }
    }
  });
  //console.log('focus input');
  $input.focus();
  //console.log('out initMergePersonnes');
}


/*
$(document).ready(function() {
  var $input = $('#acmergepersonne');
  var $eid = $('#personneeid');
  console.log("hem");
  console.log($eid.val());
  console.log("call initMergePersonnes");
  initMergePersonnes();
});

*/
