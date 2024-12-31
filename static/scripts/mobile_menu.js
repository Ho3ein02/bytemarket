const navBtn = document.querySelector(".menu-icon");
const navMenu = document.querySelector(".nav-menu");
let navOpen = false;

navBtn.addEventListener("click",function () {
    if (navOpen) {
        navBtn.classList.remove("menu-icon--open")
        navMenu.classList.remove("nav-menu--open")
        navOpen = false
    } else {
        navBtn.classList.add("menu-icon--open")
        navMenu.classList.add("nav-menu--open")
        navOpen = true
    }
})
