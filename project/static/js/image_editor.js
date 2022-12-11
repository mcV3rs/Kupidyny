/* Constants variables */
// Const for document elements
const addImg = document.getElementById('add-image');
const collection = Array.from(document.getElementsByClassName("uploaded-img"));
const lastElement = Array.from(collection)[Array.from(collection).length - 1];

// Const for File Robot Image Editor
const container = document.getElementById("image-editor");
const config = {
    source: lastElement.src,
    useBackendTranslations: true,
    language: "pl"
};
const ImageEditor = new window.FilerobotImageEditor(container, config);

/* Document main function */
document.onreadystatechange = () => {
    // Add event listener for pictures
    collection.forEach(function (element) {
        element.onclick = () => toggleActiveImage(element, element.src);
    });

    // Add data attribute for last picture and render it to editor
    lastElement.setAttribute('data-image-editor-active-image', '');
    ImageEditor.render({source: lastElement.src});
};

// TODO funkcja do opanowania
/* Image Editor render and save function */
ImageEditor.render({
    observePluginContainerSize: true,
    onSave: (imageInfo, designState) => {
        const tmpLink = document.createElement("a");
        tmpLink.download = imageInfo.fullName;
        tmpLink.href = imageInfo.imageBase64;
        tmpLink.style = "position: absolute; z-index: -111; visibility: none;";
        document.body.appendChild(tmpLink);
        tmpLink.click();
        document.body.removeChild(tmpLink);
    }
});

/* Functions */
function toggleActiveImage(imageContainer, imageSrc) {
    const removeResizeParamRegex = /\?.+/g;
    const imageUrl = imageSrc.replace(removeResizeParamRegex, '');
    const prevImageContainer = document.querySelector(
        '[data-image-editor-active-image]',
    );

    if (prevImageContainer) {
        prevImageContainer.removeAttribute('data-image-editor-active-image');
    }

    imageContainer.setAttribute('data-image-editor-active-image', '');

    ImageEditor.render({source: imageUrl});
}

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

function uploadImg(event) {
    const fd = new FormData();
    fd.append('file', event.target.files[0])

    const req = fetch('/file/upload', {
        mode: 'no-cors',
        method: 'post',
        body: fd
    });

    req.then(function (response) {
        if (!response.ok) {
            console.log(response)
        }
    }, function (error) {
        console.log(error)
        console.error('failed due to network error or cross domain')
    })

    const imageSrc = URL.createObjectURL(event.target.files[0]);

    const imageContainer = appendImageToContainer(imageSrc);

    toggleActiveImage(imageContainer, imageSrc);

    ImageEditor.render({source: imageSrc});
}

/* Event listeners */
addImg.addEventListener('change', uploadImg);
