clicked_ids = [];
function onCharacterClicked(id) {
  // console.log(id);
  grid_text = document.getElementById(id);

  if (clicked_ids.length > 4) {
    alert("not possible");
  }

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
}

function submitChoices() {
  if (clicked_ids.length > 0) {
    console.log(clicked_ids);
  }
}
