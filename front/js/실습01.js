function f01() {
  c = document.querySelector("#color01").value;
  x = document.querySelector("#target01");
  console.log(x);
  x.style.backgroundColor = c;
}

function f02(num) {
  x = document.querySelector("#target02");
  x.style.width = num + "px";
  x.style.height = num + "px";
}

function f03() {
  input31 = document.querySelector("#input31").value;
  input32 = document.querySelector("#input32").value;
  input33 = document.querySelector("#input33").value;
  resultArea = document.querySelector("#result-area");

  s = "구매자 : " + input31 + ", 상품명 : " + input32 + " , 가격 : " + input33;
  resultArea.innerHTML = s;
}

function makeTable() {
  r = prompt("row ? ");
  result = document.querySelector("#result");
  s = "";
  s += `<table border='1'><tbody>`;
  for (let i = 0; i < r; ++i) {
    s += `<tr><td>1</td><td>2</td><td>3</td></tr>`;
  }
  s += `</tbody></table>`;
  result.innerHTML = s;
}
