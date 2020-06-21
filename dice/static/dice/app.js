clicked_ids = [];
function onCharacterClicked(id) {
  // console.log(id);
  grid_text = document.getElementById(id);

  if (clicked_ids.length < 5) {
    if (grid_text.classList.contains("grid-item-selected")) {
      const index = clicked_ids.indexOf(id);
      if (index > -1) {
        clicked_ids.splice(index, 1);
      }
      grid_text.classList.remove("grid-item-selected");
      grid_text.classList.add("grid-item");
    } else {
      clicked_ids.push(id);
      grid_text.classList.add("grid-item-selected");
      grid_text.classList.remove("grid-item");
    }
  } else {
    alert("Too many characters selected, you can only have four allies");
  }
}

function submitChoices(url, pk) {
    window.open(url);
    $.get('YOUR_VIEW_HERE/'+pk+'/', function (data) {
        alert("counter updated!");
    });
}
