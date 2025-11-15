import { useAuth } from "@/contexts/AuthContext";
import { Button } from "./ui/button";
import { useContext } from "react";
import { useNavigate } from "react-router-dom";

const API_URL = import.meta.env.VITE_API_URL


export default function LogoutButton(){
    const { setUser } = useAuth()
    const navigate = useNavigate();
    
    async function handleClick(e){
        e.preventDefault()
        const res = await fetch(`${API_URL}/auth/logout`, {
            method: "POST",
            credentials: "include", // send cookies, receive Set-Cookie
        });

        if (!res.ok) {
            throw new Error(`Logout request failed: ${res.status}`);
        }

        await navigate("/")

        setUser(null)

    }

    return (
        <Button onClick={handleClick}>Logout</Button>
    )
}