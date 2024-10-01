const btn = document.querySelector('#btn')
const sidebar = document.querySelector('.sidebar')
const search = document.querySelector('.bx-search-alt')


btn.onclick = function() {
    sidebar.classList.toggle("active")
    menuBtnChange();
}

search.onclick = function() {
    sidebar.classList.toggle("active")
}

function menuBtnChange() {
    if(sidebar.classList.contains("active")){
      btn.classList.replace("bx-menu", "bx-menu-alt-right");//replacing the iocns class
    }else {
      btn.classList.replace("bx-menu-alt-right","bx-menu");//replacing the iocns class
    }
   }
