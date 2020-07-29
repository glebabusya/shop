function CategoryDropdown() {
    document.getElementById("Category-Dropdown").classList.toggle("show");
}

window.onclick = function(event) {
  if (!event.target.matches('.button')) {

    var dropdowns = document.getElementsByClassName("category-dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}