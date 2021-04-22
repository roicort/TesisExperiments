var frame = new XMLHttpRequest();
frame.open("GET", "https://raw.githubusercontent.com/roicort/TesisGraphlets/master/baseline/results/Baseline-WARD.dendrogram.html", true);
frame.onreadystatechange = function() {
  if (frame.readyState === 4) {  // Makes sure the document is ready to parse.
    if (frame.status === 200) {  // Makes sure it's found the file.
      htf = frame.responseText;
      document.getElementById('myframe').innerHTML = htf;
      console.log(htf);
    }
  }
}
frame.send(null);
