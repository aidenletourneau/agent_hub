"use client"

export function GoogleOauthButton() {
  const handleLogin = () => {
    // Redirect user to your backend’s Google OAuth route
    window.location.href = "http://localhost:8000/auth/googleLogin";
  };

  return (
    <button
      onClick={handleLogin}
      className="px-4 py-2 bg-white border border-gray-300 rounded-md flex items-center gap-2 hover:bg-gray-100"
    >
      <img
        src="https://developers.google.com/identity/images/g-logo.png"
        alt="Google logo"
        className="w-5 h-5"
      />
      <span>Sign in with Google</span>
    </button>
  );
}