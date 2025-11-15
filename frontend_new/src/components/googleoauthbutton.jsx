import { Button } from "./ui/button";

const API_URL = import.meta.env.VITE_API_URL


export function GoogleOauthButton() {
  
    const handleLogin = async (e) => {
    e.preventDefault()
    window.location.href = `${API_URL}/auth/googleLogin`;
  };

  return (
    <Button onClick={handleLogin}>
      <img
        src="https://developers.google.com/identity/images/g-logo.png"
        alt="Google logo"
        className="w-5 h-5"
      />
      Sign in with Google
    </Button>
  );
}