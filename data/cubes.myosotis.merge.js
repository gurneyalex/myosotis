CubicWeb.require('ajax.js');

function cancelSelectedMergePersonne(eid) {
    var holder = jQuery('#personnemergeformholder' + eid);
    $('#acmergepersonne').val('');
    holder.children("div#personne_entities_holder").empty();
    toggleVisibility("sgformbuttons");
}

function mergePersonnes(eid) {
    var $input = $('#personnemergeformholder' + eid + ' input')[0];
    var otherEid = $('input[name=selected-personne]').attr('value');
    var name = $('#acmergepersonne').val().strip(',');
    var d = asyncRemoteExec('merge_personnes', eid, otherEid);
    d.addCallback(
        function() {
            window.open('\/'+eid, '_self');
   });

}

function personneToMergeSelector(eid) {
  var $holder = $('#personnemergeformholder' + eid);
  var name = $('#acmergepersonne').val().strip(',');
  var entities = asyncRemoteExec("personne_entity_html", eid, name);
  entities.addCallback(function  (entitieslist) {
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
  var $input = $('#acmergepersonne');
  var personneeid = $('#personneeid').val();
  $input.keypress(function (event) {
    if (event.keyCode == KEYS.KEY_ENTER) {
      if ($input.val()){
        if ($('#sgformbuttons').hasClass('hidden')){
          toggleVisibility('sgformbuttons');
        }
        personneToMergeSelector(personneeid);
      }
    }
  });
  $input.focus();
}
