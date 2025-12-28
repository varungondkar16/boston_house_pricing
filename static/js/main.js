document.addEventListener('DOMContentLoaded', ()=>{
  const form = document.getElementById('predictForm');
  const resultBox = document.getElementById('resultBox');
  const fillBtn = document.getElementById('fillExample');

  const featureOrder = ['CRIM','ZN','INDUS','CHAS','NOX','RM','AGE','DIS','RAD','TAX','PTRATIO','LSTAT'];

  fillBtn.addEventListener('click', ()=>{
    const example = [0.00632,18.0,2.31,0,0.538,6.575,65.2,4.09,1,296,15.3,4.98];
    featureOrder.forEach((k,i)=>{
      const el = form.elements[k]; if(el) el.value = example[i];
    });
  });

  form.addEventListener('submit', async (e)=>{
    e.preventDefault();
    resultBox.textContent = 'Requesting prediction...';

    // collect values in the expected order
    const values = featureOrder.map(k => {
      const v = form.elements[k].value;
      return v === '' ? null : parseFloat(v);
    });

    if (values.some(v => v === null || Number.isNaN(v))) {
      resultBox.textContent = 'Please fill all fields with valid numbers.'; return
    }

    try {
      const resp = await fetch('/predict_api', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ data: values })
      });

      const ctype = resp.headers.get('content-type') || '';
      if (ctype.includes('application/json')) {
        const json = await resp.json();
        if (!resp.ok) {
          resultBox.textContent = 'Error: ' + (json.error || JSON.stringify(json)); return
        }
        resultBox.textContent = 'Predicted price: ' + (json.prediction ?? JSON.stringify(json));
      } else {
        // non-JSON response (likely an HTML error page)
        const text = await resp.text();
        if (!resp.ok) {
          resultBox.textContent = `Server error ${resp.status}: ${text.substring(0,200)}`;
        } else {
          resultBox.textContent = 'Unexpected response: ' + text.substring(0,200);
        }
      }
    } catch (err) {
      resultBox.textContent = 'Request failed: ' + err.message;
    }
  });
});
