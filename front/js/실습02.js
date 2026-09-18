function f01(x) {
  console.log("h1 clicked ~~~", x);
}

function changeColor(s) {
  const h1tag = document.querySelector("h1");
  // h1tag.classList.remove("red", "blue", "green");
  // h1tag.setAttribute("aaa", "bbb");
  h1tag.removeAttribute("class");
  h1tag.classList.add(s);
}
