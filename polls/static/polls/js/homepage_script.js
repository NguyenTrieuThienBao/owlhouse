let moon = document.getElementById("moon");
let text = document.getElementById("text");
let train = document.getElementById("name_train");

let desert_moon = document.getElementById("desert_moon");
let ship = document.getElementById("ship");

window.addEventListener("scroll",()=>{
    let value = window.scrollY;
    moon.style.top = value * .5 + "px";
    text.style.top = 80 + value * -0.2 + "%";
    train.style.left = value + 1.5 + "px";

    desert_moon.style.top = value * .3 + "px";
    ship.style.left = value * .6 + "px";
})
 // progress bar
 let calcScrollValue = ()=> {
    let scrollProgress = document.getElementById("progress");
    let pos = document.documentElement.scrollTop;
    
    let calcHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    let scrollValue = Math.round((pos * 100)/calcHeight);

    if(pos > 100){
        scrollProgress.style.display = "grid";
    }else{
        scrollProgress.style.display = "none";
    }
    scrollProgress.addEventListener("click",()=>{
        document.documentElement.scrollTop = 0;
    });
    scrollProgress.style.background = `conic-gradient(#194eb9 ${scrollValue}%,#67ccff ${scrollValue}%)`;
 };
 window.onscroll = calcScrollValue;
 window.onload = calcScrollValue;

let myMenu = document.getElementById("bx-menu");
let myClassMenu = document.getElementById("menu");

myMenu.addEventListener("click", function () {
  myClassMenu.classList.toggle("show");
});

//Xử lí button của thể loại sách
let myTheLoai = document.getElementById("the-loai-chevron-down");
let myClassTheLoai = document.getElementById("the-loai");

myTheLoai.addEventListener("click", function () {
  myClassTheLoai.classList.toggle("show");
});

//Xử lí button của nhà xuất bản
let myNXB = document.getElementById("NXB-chevron-down");
let myClassNXB = document.getElementById("NXB");

myNXB.addEventListener("click", function () {
  myClassNXB.classList.toggle("show");
});

const blockinfo_box = document.getElementsByClassName('info-box')[0];
const toggleButton_readmore = document.getElementsByClassName('btn')[0];
const more = document.getElementsByClassName('more')[0];
const dots = document.getElementsByClassName('dots')[0];

toggleButton_readmore.addEventListener('click', function () {
  if (blockinfo_box.classList.contains('collapsed')) {
    blockinfo_box.classList.remove('collapsed');
    blockinfo_box.classList.add('extended');
    dots.style.display = 'none';
    more.style.display = 'inline';
    toggleButton_readmore.textContent = 'Ẩn';
  } else {
    blockinfo_box.classList.remove('extended');
    more.style.display = 'none';
    dots.style.display = 'inline';
    blockinfo_box.classList.add('collapsed');
    toggleButton_readmore.textContent = 'Đọc thêm!';
  }
});
