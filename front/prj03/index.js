function f01() {
  const x = {
    nick: "Gdragon",
  };

  fetch("http://192.168.40.3:8000/hello", {
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

async function f02() {
  const resp = await fetch("http://192.168.40.3:8000/hello", {
    method: "post",
    headers: {
      "Content-Type": "application/json",
    },
    // 알림창 띄우기 시도
    body: JSON.stringify({
      nick: "<b style='color:red; font-size:30px;'>빨간닉네임</b>",
    }),
  });
  const data = await resp.json();
  console.log(data);
}
