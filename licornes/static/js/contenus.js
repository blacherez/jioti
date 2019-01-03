function remplacerMap(url) {

    //$("#map").html(url);
    //$( "#map" ).html('<iframe width="560" height="315" src="https://www.youtube.com/embed/ixv_6mJuaSY" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>');
    $.get( url, function( data ) {
      $( "#map" ).html( "<p>" + data["localisation"] + " (" + data["date"] + ")</p>" + data["media"] );
      //alert( data["media"] );
       });

}
