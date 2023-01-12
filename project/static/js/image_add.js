/* Constants variables */
// Const for document elements
const addImg_btn = document.getElementById('add-image');
const collection = Array.from(document.getElementsByClassName("uploaded-img"));

/* Functions */
function appendImageToContainer(imageSrc) {
    const imagesWrapper = document.querySelector('.uploaded-imgs');
    const imageWrapper = document.createElement('img');

    imageWrapper.src = imageSrc;

    imageWrapper.className = 'uploaded-img';

    imageWrapper.onclick = () => toggleActiveImage(imageWrapper, imageSrc);

    imagesWrapper.appendChild(imageWrapper);
    imagesWrapper.scrollTop = imagesWrapper.scrollHeight;

    return imageWrapper;
}

function addImg(event) {
    const imageSrc = URL.createObjectURL(event.target.files[0]);

    const imageContainer = appendImageToContainer(imageSrc);
}

/* Event listeners */
addImg_btn.addEventListener('change', addImg);

/* Document main function */
document.onreadystatechange = () => {
    // Add event listener for pictures
    collection.forEach(function (element) {
        element.onclick = () => toggleActiveImage(element, element.src);
    });

    // Add data attribute for last picture and render it to editor
    // lastElement.setAttribute('data-image-editor-active-image', '');
    // ImageEditor.render({source: lastElement.src});
};
