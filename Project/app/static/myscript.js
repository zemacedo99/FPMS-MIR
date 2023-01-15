function showDropdown() {
    var checkbox = document.getElementById("checkBox_id");
    var dropdown = document.getElementById("dropdown_BGR");
    // console.log(checkbox)
    // console.log(dropdown)
    if (checkbox.checked) {
        dropdown.style.display = "block";
    } else {
        dropdown.style.display = "none";
    }

}