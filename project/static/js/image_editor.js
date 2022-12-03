const container = document.getElementById("image-editor");
const config = {
    source: "https://scaleflex.cloudimg.io/v7/demo/river.png",
    useBackendTranslations: true,
    language: "pl"
};
const ImageEditor = new window.FilerobotImageEditor(container, config);

ImageEditor.render({
    // additional config provided while rendering
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