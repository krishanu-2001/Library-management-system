function searchFunc(){
  var searchText = document.querySelectorAll('#searchText')[0].value
  if(searchText != "")
    window.location = `/books/search/${searchText}\#newSearch`;
  else{
    window.location = `/books/search/\%02\%03\#newSearch`;
  }
}