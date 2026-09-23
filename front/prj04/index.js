async function getBoardInfo() {
  const resp = await fetch(`http://192.168.40.97:8001/book`, {});
  const data = await resp.json();

  const resultArea = document.querySelector("#result-area");
  resultArea.innerHTML = `title : ${data.title}, price : ${data.price}`;
}
