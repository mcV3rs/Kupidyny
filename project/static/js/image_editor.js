// TODO porządek w pliku

const container = document.getElementById("image-editor");

const addImg = document.getElementById('add-image');
const collection = document.getElementsByClassName("uploaded-img");
let lastElement = Array.from(collection)[Array.from(collection).length - 1];

const config = {
    source: lastElement.src,
    useBackendTranslations: true,
    language: "pl"
};
const ImageEditor = new window.FilerobotImageEditor(container, config);

document.onreadystatechange = () => {
    Array.from(collection).forEach(function (element) {
        element.onclick = () => toggleActiveImage(element, element.src);
    });

    lastElement.setAttribute('data-image-editor-active-image', '');
    ImageEditor.render({source: lastElement.src});
};

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
    const imagesWrapper = document.querySelector('.uploaded-imgs-wrapper');
    const imageWrapper = document.createElement('img');

    imageWrapper.src = imageSrc;

    imageWrapper.className = 'uploaded-img';

    imageWrapper.onclick = () => toggleActiveImage(imageWrapper, imageSrc);

    imagesWrapper.appendChild(imageWrapper);
    imagesWrapper.scrollTop = imagesWrapper.scrollHeight;

    return imageWrapper;
}

function uploadImg(event) {
    const imageSrc = URL.createObjectURL(event.target.files[0]);

    const imageContainer = appendImageToContainer(imageSrc);

    toggleActiveImage(imageContainer, imageSrc);

    ImageEditor.render({source: imageSrc});
}

addImg.addEventListener('change', uploadImg);
