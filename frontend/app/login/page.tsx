"use client"

import { useState } from "react";

function GoogleLoginButton() {
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

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <form
        onSubmit={handleSubmit}
        className="bg-white p-6 rounded-lg shadow-md w-80 flex flex-col gap-3"
      >
        <h1 className="text-2xl font-semibold text-center mb-2">Login</h1>

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="border p-2 rounded"
          required
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="border p-2 rounded"
          required
        />

        <button
          type="submit"
          className="bg-blue-500 hover:bg-blue-600 text-white py-2 rounded transition"
        >
          Sign In
        </button> <br></br>

        <GoogleLoginButton></GoogleLoginButton>


      </form>
    </div>
  );
}

