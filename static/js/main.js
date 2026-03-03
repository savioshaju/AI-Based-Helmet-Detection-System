document.addEventListener("DOMContentLoaded", () => {
  
    const imageInput = document.getElementById("imageInput");
    const processImageBtn = document.getElementById("processImageBtn");
    const imagePlaceholder = document.getElementById("imagePlaceholder");
    const imageResult = document.getElementById("imageResult");
    const imageLoading = document.getElementById("imageLoading");

    processImageBtn.addEventListener("click", () => {
        if (imageInput.files.length === 0) {
            alert("Please select an image file first.");
            return;
        }

        const formData = new FormData();
        formData.append("image", imageInput.files[0]);

        imagePlaceholder.classList.add("hidden");
        imageResult.classList.add("hidden");
        
        imageLoading.classList.remove("hidden");
        imageLoading.classList.add("flex");

        fetch("/upload_image", {
            method: "POST",
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            imageLoading.classList.add("hidden");
            imageLoading.classList.remove("flex");
            
            if (data.image) {
                imageResult.src = `data:image/jpeg;base64,${data.image}`;
                imageResult.classList.remove("hidden");
            } else if (data.error) {
                alert(`Detection Error: ${data.error}`);
                imagePlaceholder.classList.remove("hidden");
            }
        })
        .catch(err => {
            imageLoading.classList.add("hidden");
            imageLoading.classList.remove("flex");
            console.error("Error processing image:", err);
            alert("An error occurred while processing the image across the network.");
            imagePlaceholder.classList.remove("hidden");
        });
    });


    const videoForm = document.getElementById("videoForm");
    const videoPlaceholder = document.getElementById("videoPlaceholder");
    const videoFrame = document.getElementById("videoFrame");
    window.hideVideoPlaceholder = () => {
        if (videoFrame.src !== "" || videoFrame.contentDocument !== null) {
            videoPlaceholder.classList.add("hidden");
        }
    };

    videoForm.addEventListener("submit", (e) => {
        videoPlaceholder.classList.add("hidden");
        videoFrame.classList.remove("hidden");
    });


  
    const startWebcamBtn = document.getElementById("startWebcamBtn");
    const stopWebcamBtn = document.getElementById("stopWebcamBtn");
    const webcamPlaceholder = document.getElementById("webcamPlaceholder");
    const webcamImg = document.getElementById("webcamImg");

    let isWebcamActive = false;

    startWebcamBtn.addEventListener("click", () => {
        if (isWebcamActive) return;
        isWebcamActive = true;
        
        webcamPlaceholder.classList.add("hidden");
        
       
        webcamImg.src = `/webcam_feed?t=${new Date().getTime()}`;
        webcamImg.classList.remove("hidden");
    });

    stopWebcamBtn.addEventListener("click", () => {
        if (!isWebcamActive && webcamImg.src === "") return;
        isWebcamActive = false;

        webcamImg.src = "";
        webcamImg.classList.add("hidden");
        
        webcamPlaceholder.classList.remove("hidden");
        webcamPlaceholder.innerHTML = "Ended. Stream connection closed.";

        fetch("/stop_webcam", { method: "POST" })
            .catch(err => console.error("Error stopping webcam on server:", err));
    });

});
