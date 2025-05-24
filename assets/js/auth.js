// Google OAuth configuration
const GOOGLE_CLIENT_ID = '{{ site.google_client_id }}';
const SCOPES = 'profile email';

// Mock user data
const MOCK_USERS = {
    'user@example.com': {
        password: 'password123',
        name: 'Demo User',
        image: 'https://ui-avatars.com/api/?name=Demo+User&background=random',
        tier: 'Free',
        credits: 100
    }
};

// Initialize Google Auth
function initGoogleAuth() {
    gapi.load('auth2', () => {
        gapi.auth2.init({
            client_id: GOOGLE_CLIENT_ID,
            scope: SCOPES
        }).then(() => {
            // Listen for sign-in state changes
            gapi.auth2.getAuthInstance().isSignedIn.listen(updateSigninStatus);
            // Handle initial sign-in state
            updateSigninStatus(gapi.auth2.getAuthInstance().isSignedIn.get());
        });
    });
}

// Update UI based on sign-in status
function updateSigninStatus(isSignedIn) {
    const authContainer = document.querySelector('.auth-container');
    const authStatus = document.querySelector('.auth-status');
    const userProfile = document.getElementById('user-profile');
    const userImage = document.getElementById('user-image');
    const userName = document.getElementById('user-name');
    const userEmail = document.getElementById('user-email');
    const userTier = document.getElementById('user-tier');
    const userCredits = document.getElementById('user-credits');
    const googleAuthButton = document.getElementById('google-auth-button');
    const emailAuthForm = document.getElementById('email-auth-form');
    const signOutButton = document.getElementById('signout-button');
    const upgradeButton = document.getElementById('upgrade-button');
    const mlModelsContainer = document.querySelector('.ml-models-container');

    if (isSignedIn) {
        const user = gapi.auth2.getAuthInstance().currentUser.get();
        const profile = user.getBasicProfile();
        const authResponse = user.getAuthResponse();

        // Update UI for signed-in state
        authContainer.style.display = 'none';
        authStatus.style.display = 'block';
        userProfile.style.display = 'flex';
        userImage.src = profile.getImageUrl();
        userName.textContent = profile.getName();
        userEmail.textContent = profile.getEmail();
        googleAuthButton.style.display = 'none';
        emailAuthForm.style.display = 'none';
        signOutButton.style.display = 'block';
        upgradeButton.style.display = 'block';
        mlModelsContainer.style.display = 'grid';

        // Store the access token
        localStorage.setItem('access_token', authResponse.access_token);

        // Update user stats (this would typically come from your backend)
        userTier.textContent = 'Free Tier';
        userCredits.textContent = 'Credits: 100';
    } else {
        // Update UI for signed-out state
        authContainer.style.display = 'block';
        authStatus.style.display = 'none';
        userProfile.style.display = 'none';
        googleAuthButton.style.display = 'block';
        emailAuthForm.style.display = 'block';
        signOutButton.style.display = 'none';
        upgradeButton.style.display = 'none';
        mlModelsContainer.style.display = 'none';

        // Clear the access token
        localStorage.removeItem('access_token');
    }
}

// Handle Google authentication
function handleGoogleAuth() {
    gapi.auth2.getAuthInstance().signIn().then(() => {
        console.log('Google authentication successful');
    }).catch((error) => {
        console.error('Google authentication failed:', error);
    });
}

// Handle email authentication
function handleEmailAuth(event) {
    event.preventDefault();
    const email = document.getElementById('email-input').value;
    const password = document.getElementById('password-input').value;

    // Here you would typically make an API call to your backend
    console.log('Email authentication:', { email, password });
}

// Sign out
function signOut() {
    gapi.auth2.getAuthInstance().signOut();
}

// Initialize mock authentication
function initMockAuth() {
    // Check for existing session
    const savedUser = localStorage.getItem('current_user');
    if (savedUser) {
        updateUIForSignedInUser(JSON.parse(savedUser));
    } else {
        updateUIForSignedOutUser();
    }
}

// Update UI based on sign-in status
function updateUIForSignedInUser(user) {
    const authContainer = document.querySelector('.auth-container');
    const authStatus = document.querySelector('.auth-status');
    const userProfile = document.getElementById('user-profile');
    const userImage = document.getElementById('user-image');
    const userName = document.getElementById('user-name');
    const userEmail = document.getElementById('user-email');
    const userTier = document.getElementById('user-tier');
    const userCredits = document.getElementById('user-credits');
    const googleAuthButton = document.getElementById('google-auth-button');
    const emailAuthForm = document.getElementById('email-auth-form');
    const signOutButton = document.getElementById('signout-button');
    const upgradeButton = document.getElementById('upgrade-button');
    const mlModelsContainer = document.querySelector('.ml-models-container');

    // Update UI for signed-in state
    authContainer.style.display = 'none';
    authStatus.style.display = 'block';
    userProfile.style.display = 'flex';
    userImage.src = user.image;
    userName.textContent = user.name;
    userEmail.textContent = user.email;
    googleAuthButton.style.display = 'none';
    emailAuthForm.style.display = 'none';
    signOutButton.style.display = 'block';
    upgradeButton.style.display = 'block';
    mlModelsContainer.style.display = 'grid';

    // Update user stats
    userTier.textContent = `${user.tier} Tier`;
    userCredits.textContent = `Credits: ${user.credits}`;
}

function updateUIForSignedOutUser() {
    const authContainer = document.querySelector('.auth-container');
    const authStatus = document.querySelector('.auth-status');
    const userProfile = document.getElementById('user-profile');
    const googleAuthButton = document.getElementById('google-auth-button');
    const emailAuthForm = document.getElementById('email-auth-form');
    const signOutButton = document.getElementById('signout-button');
    const upgradeButton = document.getElementById('upgrade-button');
    const mlModelsContainer = document.querySelector('.ml-models-container');

    // Update UI for signed-out state
    authContainer.style.display = 'block';
    authStatus.style.display = 'none';
    userProfile.style.display = 'none';
    googleAuthButton.style.display = 'block';
    emailAuthForm.style.display = 'block';
    signOutButton.style.display = 'none';
    upgradeButton.style.display = 'none';
    mlModelsContainer.style.display = 'none';

    // Clear stored user data
    localStorage.removeItem('current_user');
}

// Handle Google authentication (mock)
function handleGoogleAuthMock() {
    // Simulate Google sign-in
    const mockUser = {
        email: 'google.user@example.com',
        name: 'Google User',
        image: 'https://ui-avatars.com/api/?name=Google+User&background=random',
        tier: 'Free',
        credits: 100
    };
    
    // Simulate API delay
    setTimeout(() => {
        localStorage.setItem('current_user', JSON.stringify(mockUser));
        updateUIForSignedInUser(mockUser);
    }, 1000);
}

// Handle email authentication (mock)
function handleEmailAuthMock(event) {
    event.preventDefault();
    const email = document.getElementById('email-input').value;
    const password = document.getElementById('password-input').value;

    // Check mock credentials
    if (MOCK_USERS[email] && MOCK_USERS[email].password === password) {
        const mockUser = {
            email: email,
            ...MOCK_USERS[email]
        };
        
        // Simulate API delay
        setTimeout(() => {
            localStorage.setItem('current_user', JSON.stringify(mockUser));
            updateUIForSignedInUser(mockUser);
        }, 1000);
    } else {
        alert('Invalid email or password');
    }
}

// Sign out
function signOutMock() {
    localStorage.removeItem('current_user');
    updateUIForSignedOutUser();
}

// Handle premium upgrade (mock)
function handleUpgrade() {
    const currentUser = JSON.parse(localStorage.getItem('current_user'));
    if (currentUser) {
        currentUser.tier = 'Premium';
        currentUser.credits = 'Unlimited';
        localStorage.setItem('current_user', JSON.stringify(currentUser));
        updateUIForSignedInUser(currentUser);
        alert('Successfully upgraded to Premium!');
    }
}

// Initialize when the page loads
document.addEventListener('DOMContentLoaded', () => {
    // Load the Google API
    const script = document.createElement('script');
    script.src = 'https://apis.google.com/js/api.js';
    script.onload = () => {
        gapi.load('client:auth2', initGoogleAuth);
    };
    document.body.appendChild(script);

    // Initialize mock authentication
    initMockAuth();

    // Add event listeners
    const googleAuthButton = document.getElementById('google-auth-button');
    const emailAuthForm = document.getElementById('email-auth-form');
    const signOutButton = document.getElementById('signout-button');
    const upgradeButton = document.getElementById('upgrade-button');

    if (googleAuthButton) {
        googleAuthButton.addEventListener('click', handleGoogleAuthMock);
    }
    if (emailAuthForm) {
        emailAuthForm.addEventListener('submit', handleEmailAuthMock);
    }
    if (signOutButton) {
        signOutButton.addEventListener('click', signOutMock);
    }
    if (upgradeButton) {
        upgradeButton.addEventListener('click', handleUpgrade);
    }
}); 
