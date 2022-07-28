function changeItemsStyle() {
    const complimentary = document.querySelector('#hly-abm-page-complimentary-jn3xd07benr');
    const items = document.querySelector('#hly-abm-page-content-izzoq7bi6q');

    const complimentaryVideo = complimentary.querySelector('.hly-complimentary-video-container');

    if (complimentaryVideo.innerHTML == "") {
        complimentary.style.display = "none";
        items.style.display = "block";
    } else {
        complimentary.style.display = "block";
        items.style.display = "none";
    }
}

setTimeout(changeItemsStyle, 1500);