  function toggleProfit(element) {
    const absValue = element.getAttribute('data-abs');
    const pctValue = element.getAttribute('data-pct');
    const isShowingAbs = element.innerText.trim().startsWith('$');

    if (isShowingAbs){
      element.innerText = pctValue + '%';

    } else {
      element.innerText = '$' + absValue;
    }
  }