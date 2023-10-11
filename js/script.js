
setInterval(() => {

  const time = dayjs().format('ddd MMM D HH:mm');

  document.getElementById('clock').innerHTML = time;

}, 500);