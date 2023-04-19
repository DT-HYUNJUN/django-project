const comments = document.querySelectorAll('#comments')

comments.forEach(comment => {
  const deleteBtn = comment.querySelector('#comment_delete')

  comment.addEventListener('mouseover', () => {
    console.log(comment)
    deleteBtn.classList.remove('hidden')
  })

  comment.addEventListener('mouseout', () => {
    console.log(comment)
    deleteBtn.classList.add('hidden')
  })
});