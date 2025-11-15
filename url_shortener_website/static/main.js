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

const BASE_URL = "http://127.0.0.1:8000"

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


const signupFormElement = document.getElementById('signupFormElement');
const loginFormElement = document.getElementById('loginFormElement');
// form message helpers and auth state
const signupMessageEl = document.getElementById('signupMessage');
const loginMessageEl = document.getElementById('loginMessage');
const dashboardBtn = document.getElementById('dashboardBtn');
const logoutBtn = document.getElementById('logoutBtn');
const downloadQrBtn = document.getElementById('downloadQrBtn');

function showFormMessage(el, msg, isError=false){
    if(!el) return;
    el.textContent = msg;
    el.style.display = 'block';
    el.className = 'form-message ' + (isError ? 'error' : 'success');
}

function clearFormMessage(el){ if(!el) return; el.textContent=''; el.style.display='none'; el.className='form-message'; }

function updateNavForLoggedIn(){
    const loggedIn = localStorage.getItem('loggedIn') === 'true';
    if(loggedIn){
        if(loginBtn) loginBtn.style.display = 'none';
        if(signupBtn) signupBtn.style.display = 'none';
        if(logoutBtn) logoutBtn.style.display = 'block';
        if(dashboardBtn) dashboardBtn.style.display = 'block';
    } else {
        if(loginBtn) loginBtn.style.display = 'block';
        if(signupBtn) signupBtn.style.display = 'block';
        if(logoutBtn) logoutBtn.style.display = 'none';
        if(dashboardBtn) dashboardBtn.style.display = 'none';
    }
}

// signup submission (AJAX)
if(signupFormElement){
    signupFormElement.addEventListener('submit', async (e)=>{
        e.preventDefault();
        clearFormMessage(signupMessageEl);
        const email = document.getElementById('signupEmail').value.trim();
        const password = document.getElementById('signupPassword').value;
        const passwordConfirm = document.getElementById('signupPasswordConfirm').value;
        if(password !== passwordConfirm){
            showFormMessage(signupMessageEl, 'Passwords do not match', true);
            return;
        }

        try{
            const resp = await fetch('/api/signup', {
                method: 'POST',
                credentials: 'same-origin',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ email: email, password: password })
            });
            const data = await resp.json();
            if(resp.status === 201){
                showFormMessage(signupMessageEl, data.success || 'Account created. Please log in.', false);
                // switch to login after short delay
                setTimeout(()=>{ openAuth('login', loginBtn); clearFormMessage(signupMessageEl); }, 900);
            } else {
                showFormMessage(signupMessageEl, data.error || 'Signup failed', true);
            }
        } catch(err){
            showFormMessage(signupMessageEl, 'Network error. Try again.', true);
        }
    });
}

// login submission (AJAX)
if(loginFormElement){
    loginFormElement.addEventListener('submit', async (e)=>{
        e.preventDefault();
        clearFormMessage(loginMessageEl);
        const email = document.getElementById('loginEmail').value.trim();
        const password = document.getElementById('loginPassword').value;

        try{
            const resp = await fetch(`/api/login`, {
                method: 'POST',
                credentials: 'same-origin',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ email: email, password: password })
            });
            const data = await resp.json();
            if(resp.status === 200){
                // mark logged in locally (skeleton)
                localStorage.setItem('loggedIn', 'true');
                localStorage.setItem('userEmail', email);
                updateNavForLoggedIn();
                showFormMessage(loginMessageEl, data.success || 'Logged in', false);
                setTimeout(()=>{ closeAuth(); clearFormMessage(loginMessageEl); }, 600);
            } else {
                showFormMessage(loginMessageEl, data.error || 'Login failed', true);
            }
        } catch(err){
            showFormMessage(loginMessageEl, 'Network error. Try again.', true);
        }
    });
}

// logout action - call server to clear session then update UI
if(logoutBtn) logoutBtn.addEventListener('click', async ()=>{
    try{
        await fetch('/api/logout', { method: 'POST', credentials: 'same-origin' });
    } catch(e){ /* ignore network errors */ }
    localStorage.removeItem('loggedIn');
    localStorage.removeItem('userEmail');
    updateNavForLoggedIn();
});

// dashboard action (redirect to server-protected dashboard)
if(dashboardBtn) dashboardBtn.addEventListener('click', ()=>{
    window.location.href = '/user/dashboard';
});

// init nav on load
updateNavForLoggedIn();


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
        xhr.open("POST", `${BASE_URL}/api/generate_shortcode`);
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

                    // show download QR button (UI only - no implementation)
                    if(downloadQrBtn){
                        downloadQrBtn.style.display = 'inline-block';
                        // store the shortcode/url for future implementation
                        downloadQrBtn.dataset.shorturl = responseJSON.success;
                    }

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