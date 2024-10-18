
function myFunction() {
    
    const hamburger = document.getElementById("menu-icon")
    const menu = document.getElementById("menu")
    const rotate = document.getElementById("angle-down")
    
    
    hamburger.addEventListener("click", () => {
        
    // if (menu.style.display == "flex") {
        
    //     menu.style.display = "none"
    // } else {
        
        
    //     menu.style.display = "flex"
    // }
    // hamburger.classList.toggle("hidden")
    menu.classList.toggle("visible")
    rotate.classList.toggle("rotated")
    })
}