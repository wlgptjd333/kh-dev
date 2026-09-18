// 선언적 함수
function f01(x, y) {
  console.log(x);
  console.log(y);
  console.log(arguments);
  console.log("f01 called ~~~");
}

f01(10, 20, 30, 40, 50);

// 익명 함수
const f02 = function () {
  console.log("anonymous func called ~~~");
};

// 화살표 함수

const f03 = () => {
  console.log("arrow function called ~~~");
};

const x = 10 / 0;
console.log(x);
// const result = isNaN(x);
const result = ifFinite(x);
console.log(result);


function f(){
  const temp = 10;
  return temp;
}
