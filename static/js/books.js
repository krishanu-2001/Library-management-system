function searchFunc(){
  var searchText = document.querySelectorAll('#searchText')[0].value
  if(searchText != "")
    window.location = `/books/search/${searchText}\#newSearch`;
  else{
    window.location = `/books/search/t\#newSearch`;
  }
}

function toggleMove(){
    var element = document.querySelectorAll('.moveTextA')
    for(let i=0;i<element.length;i++)
	   	element[i].classList.toggle("moveText");

    element = document.querySelectorAll('.moveBoxA')
    for(let i=0;i<element.length;i++)
	   	element[i].classList.toggle("moveBox");
}

function moveBook(shelf_id){
  assert(shelf_id)
}