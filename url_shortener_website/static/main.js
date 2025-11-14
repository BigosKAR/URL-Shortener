let shortenButton = document.getElementById("shortenButton")
let copyButton = document.getElementById("copyButton")

// Auth modal controls
const loginBtn = document.getElementById("loginBtn");
const signupBtn = document.getElementById("signupBtn");
const authOverlay = document.getElementById("authOverlay");
const authClose = document.getElementById("authClose");
const authBox = document.getElementById("authBox");
const loginFormBox = document.getElementById("loginForm");
const signUpFormBox = document.getElementById("signUpForm");
const showSignupLink = document.getElementById("showSignup");
const showLoginLink = document.getElementById("showLogin");

function openAuth(which, anchorEl){
    // show overlay (prevents page interaction)
    if(!authOverlay) return;
    authOverlay.style.display = 'block';
    authOverlay.setAttribute('aria-hidden','false');

    // choose which form to show
    if(which === 'login'){
        if(loginFormBox) loginFormBox.style.display = 'block';
        if(signUpFormBox) signUpFormBox.style.display = 'none';
    } else {
        if(loginFormBox) loginFormBox.style.display = 'none';
        if(signUpFormBox) signUpFormBox.style.display = 'block';
    }

    // position the auth box under the anchor button (if provided)
    if(authBox){
        authBox.style.position = 'fixed';
        authBox.style.left = '';
        authBox.style.right = '';
        authBox.style.top = '';
        authBox.style.transform = '';

        if(anchorEl && typeof anchorEl.getBoundingClientRect === 'function'){
            const rect = anchorEl.getBoundingClientRect();
            // place just below the button
            const top = rect.bottom + 6; // 6px gap
            // align right edges
            const right = window.innerWidth - rect.right;
            authBox.style.top = top + 'px';
            authBox.style.right = right + 'px';
        } else {
            // default fallback: top-right corner under nav
            authBox.style.top = '56px';
            authBox.style.right = '16px';
        }
    }
}

function closeAuth(){
    if(!authOverlay) return;
    authOverlay.style.display = 'none';
    authOverlay.setAttribute('aria-hidden','true');
    if(authBox){
        authBox.style.top = '';
        authBox.style.right = '';
    }
}

if(loginBtn) loginBtn.addEventListener('click', (e)=> openAuth('login', e.currentTarget));
if(signupBtn) signupBtn.addEventListener('click', (e)=> openAuth('signup', e.currentTarget));
if(authClose) authClose.addEventListener('click', closeAuth);
if(authOverlay) authOverlay.addEventListener('click', (e)=>{ if(e.target === authOverlay) closeAuth(); });
if(showSignupLink) showSignupLink.addEventListener('click', (e)=>{ e.preventDefault(); openAuth('signup', signupBtn || loginBtn); });
if(showLoginLink) showLoginLink.addEventListener('click', (e)=>{ e.preventDefault(); openAuth('login', loginBtn || signupBtn); });

// simple signup client-side validation
const signupFormElement = document.getElementById('signupFormElement');
if(signupFormElement){
    signupFormElement.addEventListener('submit', (e)=>{
        e.preventDefault();
        const pw = document.getElementById('signupPassword').value;
        const pw2 = document.getElementById('signupPasswordConfirm').value;
        if(pw !== pw2){
            alert('Passwords do not match');
            return;
        }
        // TODO: submit to backend endpoint
        alert('Signup submitted (client-side).');
        closeAuth();
    });
}

// simple login handler (client-side placeholder)
const loginFormElement = document.getElementById('loginFormElement');
if(loginFormElement){
    loginFormElement.addEventListener('submit', (e)=>{
        e.preventDefault();
        // TODO: submit to backend endpoint
        alert('Login submitted (client-side).');
        closeAuth();
    });
}

shortenButton.addEventListener("click", () => {
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
//         xhr.onerror = function() { // only triggers if the request couldn't be made at all
//             
        // };
    }
})

copyButton.addEventListener("click", () => {
    let shortUrlElement = document.getElementById("shortUrl");
    navigator.clipboard.writeText(shortUrlElement.innerHTML);

    alert("Copied to the clipboard")
})