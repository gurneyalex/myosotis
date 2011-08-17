CubicWeb.require('ajax.js');

function cancelSelectedMergePersonne(eid) {
    console.log('cancel merge');
    var holder = jQuery('#personnemergeformholder' + eid);
    jQuery('#acmergepersonne').val('');
    holder.children("div#personne_entities_holder").empty();
    toggleVisibility("sgformbuttons");
}

function mergePersonnes(eid) {
    console.log('do merge');
    var input = jQuery('#personnemergeformholder' + eid + ' input')[0];
    var name = jQuery('#acmergepersonne').val().strip(',');
    console.log("call merge personnes ", eid, name);
    var d = asyncRemoteExec('merge_personnes', eid, name);

    d.addCallback(function(personneprimaryview) {
      var dom = getDomFromResponse(personneprimaryview);
      //jQuery('#contentmain').replaceWith(dom);
      jQuery('#contentmain').empty().append(dom);
      if (jQuery('#sgformbuttons').hasClass('hidden') == false){
         toggleVisibility("sgformbuttons");
       }
      updateMessage(_("personne has been merged with ")+ name );
      buildWidgets();
      initMergePersonnes();
   });

}

function personneToMergeSelector(eid) {
  console.log('personne to merge selector');
  var holder = jQuery('#personnemergeformholder' + eid);
  var name = jQuery('#acmergepersonne').val().strip(',');
  var entities = asyncRemoteExec("personne_entity_html", name);
  entities.addCallback(function  (entitieslist) {
    log(entitieslist);
    var dom = getDomFromResponse(entitieslist);
    jQuery('#personne_entities_holder').empty().append(dom);
    if( jQuery("#personne_entities_holder").find('div#personneEntities').length ) {
        jQuery('#sgformbuttons').show();}
    else{
      jQuery('#sgformbuttons').hide();
    }
    });
  jQuery('#acmergepersonne').focus();
};

function initMergePersonnes(){
  console.log('initMergePersonnes');
  var input = jQuery('#acmergepersonne');
  var personneeid = jQuery('#personneeid').val();
  console.log('personne eid ', personneeid );
  console.log(input.length);
  input.keypress(function (event) {
    console.log("blaa");
    console.log(input.val());
    if (event.keyCode == KEYS.KEY_ENTER) {
      if (input.val()){
        if (jQuery('#sgformbuttons').hasClass('hidden')){
          toggleVisibility('sgformbuttons');
        }
        personneToMergeSelector(personneeid);
      }
    }
  });
  console.log('focus input');
  jQuery(input).focus();
  console.log('out initMergePersonnes');
}



$(document).ready(function() {
  var input = jQuery('#acmergepersonne');
  var eid = jQuery('#personneeid');
  console.log("hem");
  console.log(eid.val());
  console.log("call initMergePersonnes");
  initMergePersonnes();
});


