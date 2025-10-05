let shortenButton = document.getElementById("shortenButton")
let copyButton = document.getElementById("copyButton")

shortenButton.addEventListener("click", () => {
    /**
     * This function is responsible for the button logic of the website.
     * The frontend will send a request to the REST API endpoint that will return a shortened URL in the case of a success and edit all the necessary styling.
     * 
     * The same goes for failure. The site will be updated appropriately and display the error message.
     */
    let userInput = document.getElementById("userInput")
    if(userInput.value !== ""){
        // defining elements we will change
        let displayErrorElement = document.getElementById("errorMessage");
        let errorContainer = document.getElementById("errorContainer")

        let displayShortUrlContainer = document.getElementById("shortUrlContainer");
        let displayShortUrlElement = document.getElementById("shortUrl");

        let displayIncorrectShortcodeElement = document.getElementById("incorrectShortcodeContainer")

        const xhr = new XMLHttpRequest();
        xhr.open("POST", "http://127.0.0.1:8000/api/generate_shortcode");
        xhr.setRequestHeader("Content-type", "application/json")
        const body = JSON.stringify({
            url: userInput.value,
        });
        xhr.send(body);
        xhr.onload = () => {
            if(xhr.status === 200 || xhr.status === 201){
                const responseJSON = JSON.parse(xhr.response)
                
                displayShortUrlContainer.style.display = "flex";

                displayShortUrlElement.href = responseJSON.success; 
                displayShortUrlElement.innerHTML = responseJSON.success;

                // Delete any previous errors
                if (displayIncorrectShortcodeElement !== null)displayIncorrectShortcodeElement.style.display = 'none'; // Shortcode might or might not exit!
                errorContainer.style.display = "none";
            }
            else if(xhr.status === 400){
                const responseJSON = JSON.parse(xhr.response)
                displayErrorElement.innerHTML = responseJSON.error;

                errorContainer.style.display = "flex";
                // Delete any previous successes or errors

                if(displayIncorrectShortcodeElement !== null)displayIncorrectShortcodeElement.style.display = 'none';
                displayShortUrlContainer.style.display = "none";
            }       
        };
    }
})

copyButton.addEventListener("click", () => {
    /**
     * Responsible for button logic for copying the shortened URL.
     */
    let shortUrlElement = document.getElementById("shortUrl");
    navigator.clipboard.writeText(shortUrlElement.innerHTML);

    alert("Copied to the clipboard")
})