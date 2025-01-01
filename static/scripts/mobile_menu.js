const navBtn = document.querySelector(".menu-icon");
const navMenu = document.querySelector(".nav-menu");
const cover = document.querySelector(".cover");
let navOpen = false;

navBtn.addEventListener("click",function () {
    if (navOpen) {
        navBtn.classList.remove("menu-icon--open")
        navMenu.classList.remove("nav-menu--open")
        cover.classList.remove("cover--show")
        navOpen = false
    } else {
        navBtn.classList.add("menu-icon--open")
        navMenu.classList.add("nav-menu--open")
        cover.classList.add("cover--show")
        navOpen = true
    }
})

cover.addEventListener('click', () => {
    navBtn.classList.remove("menu-icon--open")
    navMenu.classList.remove("nav-menu--open")
    cover.classList.remove("cover--show")
    navOpen = false
})
