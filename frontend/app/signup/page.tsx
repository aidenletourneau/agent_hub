"use client"

import { useState } from "react";
import { SigninForm } from "@/components/ui/signin-form";



export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log("Email:", email);
    console.log("Password:", password);
    // You can call your backend API here (e.g., fetch('/api/login', ...))
  };

  return (
    <>
        <SigninForm></SigninForm>
    </>
  );
}

