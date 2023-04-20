const form = document.querySelector('#follow-form')
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

form.addEventListener('submit', (e) => {
  e.preventDefault()
  const userId = e.target.dataset.userId
  axios({
    method: 'post',
    url: `/accounts/${userId}/follow/`,
    headers: {'X-CSRFToken': csrftoken}
  })
    .then((response) => {
      const followBtn = document.querySelector('#follow-form > input[type=submit]')
      const isFollowed = response.data.is_followed
      if (isFollowed === true) {
        followBtn.value = '팔로잉'
        followBtn.classList.remove('btn-primary')
        followBtn.classList.add('btn-secondary')
      } else {
        followBtn.value = '팔로우'
        followBtn.classList.remove('btn-secondary')
        followBtn.classList.add('btn-primary')
      }
      const followingsCountTag = document.getElementById('followings-count')
      const followersCountTag = document.getElementById('followers-count')
      const followingsCountData = response.data.followings_count
      const followersCountData = response.data.followers_count
      followingsCountTag.textContent = followingsCountData
      followersCountTag.textContent = followersCountData
    })
})




// followerModals.forEach(followerModal => {
//   followerModal.addEventListener('submit', (e) => {
//     e.preventDefault()

//   })
// });

// const forms = document.querySelectorAll('#follow-form');
// const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

// forms.forEach((form) => {
//   form.addEventListener('submit', (e) => {
//     e.preventDefault();
//     const userId = e.target.dataset.userId;
//     axios({
//       method: 'post',
//       url: `/accounts/${userId}/follow/`,
//       headers: {'X-CSRFToken': csrftoken}
//     })
//       .then((response) => {
//         const isFollowed = response.data.is_followed;
//         const followBtn = form.querySelector('input[type=submit]');
//         if (isFollowed === true) {
//           followBtn.classList.remove('btn-primary');
//           followBtn.classList.add('btn-secondary');
//           followBtn.value = '팔로잉';
//         } else {
//           followBtn.classList.remove('btn-secondary');
//           followBtn.classList.add('btn-primary');
//           followBtn.value = '팔로우';
//         }
//         const followingsCountTag = document.getElementById('followings-count');
//         const followersCountTag = document.getElementById('followers-count');
//         const followingsCountData = response.data.followings_count;
//         const followersCountData = response.data.followers_count;
//         followingsCountTag.textContent = followingsCountData;
//         followersCountTag.textContent = followersCountData;
//       });
//   });
// });