function showDropdown(checkbox_id) {
    // console.log(checkbox_id)
    var dropdown_id = checkbox_id.replace("checkBox", "dropdown");
    var checkbox = document.getElementById(checkbox_id);
    var dropdown = document.getElementById(dropdown_id);
    // console.log(checkbox)
    // console.log(dropdown)
    if (checkbox.checked) {
        dropdown.style.display = "block";
    } else {
        dropdown.style.display = "none";
    }

}