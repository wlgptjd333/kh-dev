// const x = {
//   title: "해리포터",
//   price: 3000,
//   writer: "조앤케이롤링",
//   price: 7000,
// };

// const s = "title";
// console.log(x["price"]);

const person = {
  name: "홍길동",
  age: 20,
  isAdult: true,
  hobbys: ["코딩", "개발", "프로그래밍"],
  eat: function () {
    console.log("오이시이");
  },
};

person.eat();

person.height = 180;
person["weight"] = 60;

console.log(person);
