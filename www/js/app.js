function setName(){
  var cname = this.text;
  document.getElementById("imglink").setAttribute("src","IAUdata/" + cname + "_IAU.svg");
  document.getElementById("detaillink").setAttribute("src","wikidata/" + cname + ".html");
  document.getElementById("imageh1").innerHTML=cname;
  document.getElementById("detailh1").innerHTML=cname;   
};

$(document).on('pagebeforecreate',"#home", function(event){
  var clist=['Andromeda',
  'Antlia','Apus','Aquarius','Aquila','Ara','Aries','Auriga','Bootes','Caelum','Camelopardalis','Cancer','CanesVenatici','CanisMajor','CanisMinor',
  'Capricornus','Carina','Cassiopeia','Centaurus','Cepheus','Cetus','Chamaeleon','Circinus','Columba','ComaBerenices','CoronaAustralis','Corvus',
  'Crater','Crux','Cygnus','Delphinus','Dorado','Draco','Equuleus','Eridanus','Fornax','Gemini','Grus','Hercules','Horologium','Hydra','Hydrus','Indus',
  'Lacerta','Leo','LeoMinor','Lepus','Libra','Lupus','Lynx','Lyra','Mensa','Microscopium','Monoceros','Musca','Norma','Octans','Ophiuchus','Orion','Pavo',
  'Pegasus','Perseus','Phoenix','Pictor','Pisces','PiscisAustrinus','Puppis','Pyxis','Reticulum','Sagitta','Sagittarius','Scorpius','Sculptor','Scutum',
  'SerpensCaput','SerpensCauda','Sextans','Taurus','Telescopium','Triangulum','TriangulumAustrale','Tucana','UrsaMajor','UrsaMinor','Vela','Virgo',
  'Volans','Vulpecula'];
  var arrayLength = clist.length;
  var listhtml = '';
  for(var i =0; i<arrayLength; i++){
    listhtml+= '<li><a href="#image" name="clist">' + clist[i] + '</a></li>';
  };
  $(listhtml).appendTo("#constellationlist").enhanceWithin();
});

document.addEventListener('DOMContentLoaded', function(){
  var elems = document.getElementsByName('clist');
  for (var i=0;i<elems.length;i++){
    elems[i].addEventListener('click',setName);
  }; 
});

$(document).on('pageshow',"#detail", function(event){
  var a = $(".ui-mobile").height();
  var b = $("#detailheader").outerHeight(true);
  var ht = a - b;
  //$("#detailcontent").height(ht).trigger("updatelayout");
  //$("#detailbody").height(ht).trigger("updatelayout");
  $("#detaillink").height(ht - 4).trigger("updatelayout"); //4px magic
});  