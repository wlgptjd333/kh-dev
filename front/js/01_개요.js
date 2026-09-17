// windows: 전역 객체
// window.alert("hello~~~!");

// console.log(123);

// x = confirm("ㄹㅇ ㅋㅋ");
// console.log(x);

// x = prompt("name ?");
// console.log(x);

// document.write("<h1>zzz</h1>");

function f01() {
  // x = document.getElementById("target");
  // x = document.queryElementsByClassName("abc");
  // x = document.querySelectorAll(".abc");
  // console.log(x);
  // x[0].innerHTML = "hello~~~";

  x = document.querySelector("input[name=title]");
  console.log(x.value);
  x.value = "오늘 점심 뭐먹지";
}
