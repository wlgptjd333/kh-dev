function f01() {
  window.open("https://www.naver.com", "abc", "width=500, height=300");
}

function f02() {
  setTimeout(() => {
    console.log("hello called ~~");
  }, 3000);
}

function f03() {
  const timer = setInterval(() => {
    console.log("interval called ~~");
  }, 1000);

  setTimeout;
  setTimeout(() => {
    clearTimeout(timer);
  }, 5000);
}

function f04() {
  // location.href = "https://www.naver.com";
  location.reload();
}

function f05() {
  history.back();
  history.forward();
  history.go(-1);
  history.go(1);
}

function f06() {
  console.log(navigator);
}

function f07() {
  console.log(screen);
}