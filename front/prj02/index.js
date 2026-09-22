function f01() {
  const x = {
    title: "해리포터",
    price: 10101,
  };

  fetch("http://192.168.40.3:8000/books", {
    method: "post",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(x),
  })
    .then((resp) => {
      console.log("resp: ", resp);
      return resp.json();
    })
    .then((data) => {
      console.log(data);
    });
}

function f02() {
  const p = new Promise((resolve, reject) => {
    console.log("서버한테 가서 데이터 받아오기~~~");
    const isSuccess = true;
    if (isSuccess) {
      resolve("성공ㅋㅋ");
    } else {
      reject("실패ㅜㅜ");
    }
  });

  p.then((temp) => {
    console.log("then called ~~~");
    console.log("temp : ", temp);
  }).catch((temp) => {
    console.log("catch called ~~~");
    console.log("temp : ", temp);
  });
  console.log(p);
}
