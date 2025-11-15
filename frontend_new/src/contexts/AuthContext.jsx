import React, { createContext, useContext, useEffect, useState } from "react";

const AuthContext = createContext();
const API_URL = import.meta.env.VITE_API_URL

export function AuthProvider({ children }) {

    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        async function restoreSession() {
            try {
                const res = await fetch(`${API_URL}/auth/me`, {
                    credentials: "include", 
                });

                if (res.ok) {
                const data = await res.json()
                    setUser(data.user);
                } else {
                    setUser(null);
                }
            } catch (err) {
                setUser(null); 
            } finally {
                setLoading(false);
            }
        }
        restoreSession(); 
    }, []);

    const value = {
        user,
        loading,
        setUser,
    };

    return (
        <AuthContext value={value}>
            {children}
        </AuthContext>
    )
}

export function useAuth() {
    return useContext(AuthContext);
}