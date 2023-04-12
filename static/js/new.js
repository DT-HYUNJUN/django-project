const newElements = document.querySelectorAll('.new')
newElements.forEach((el) => {
  setInterval(() => {
    el.classList.toggle('text-danger')
  }, 800)
})