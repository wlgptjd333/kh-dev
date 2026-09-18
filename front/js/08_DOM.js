function f01() {
  const elemNode = document.createElement("h3");
  console.log(elemNode);
  const textNode = document.createTextNode("hello~~~");
  console.log(textNode);

  elemNode.appendChild(textNode);

  console.log(elemNode);

  const bodyTag = document.querySelector("body");
  bodyTag.appendChild(elemNode);
}
