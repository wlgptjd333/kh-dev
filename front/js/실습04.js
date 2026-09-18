// const x = document.querySelector(".test");
// console.log(x);

// const y = document.querySelector("#t");
// console.log(y);

// const z = document.querySelectorAll("input[name=title]");
// console.log(z);

//const x = document.querySelector("")

// 리스트 중 2번째 요소
// const a = document.querySelector("li:nth-child(2)");

// 클래스가 item인 요소 근데 태그명은 div 여야됨.
// const b = document.querySelector("div.item");

// form 태그 내 input 태그 중 name 이 username 인 요소
// const c = document.querySelector("form input[name='username']");

// console.log(a);
// console.log((b.innerHTML = "<h1>asdfasdf</h1>"));
// console.log(c);

// const x = document.querySelector("input[type=text]");
// console.log(x.value);

const x = document.querySelector("#target");
console.log(x);

function f01() {
  console.log(11);
  const x = document.querySelector("#target");
  x.classList.toggle("gray");
}
