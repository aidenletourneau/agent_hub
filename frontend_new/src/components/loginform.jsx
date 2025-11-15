import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { z } from "zod"
import { GoogleOauthButton } from "./googleoauthbutton"
import { Button } from "@/components/ui/button"
import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
    } from "@/components/ui/form"
    import { Input } from "@/components/ui/input"
import { useNavigate } from "react-router"
import { useAuth } from "@/contexts/AuthContext"

const formSchema = z.object({
    username: z.string().min(2, {
        error: "Username must be at least 2 characters.",
    }),
    password: z.string()
})

const API_URL = import.meta.env.VITE_API_URL

export default function LoginForm() {
    const { setUser } = useAuth()
    const navigate = useNavigate()
    const form = useForm({
        resolver: zodResolver(formSchema),
        defaultValues: {
            username: "",
            password: ""
        }
    })

    async function onSubmit(values){
        console.log(values)
        const res = await fetch(`${API_URL}/auth/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(values),
            credentials: "include",
        })

        if (!res.ok){
            throw new Error(`Request failed: ${res.status}`);
        }

        const data = await res.json()

        
        setUser(data.user)

        navigate("/")
    }

    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
                <FormField
                control={form.control}
                name="username"
                render={({ field }) => (
                    <FormItem>
                    <FormLabel>Username</FormLabel>
                    <FormControl>
                        <Input placeholder="Username" {...field} />
                    </FormControl>
                    <FormMessage />
                    </FormItem>
                )}
                />
                <FormField
                control={form.control}
                name="password"
                render={({ field }) => (
                    <FormItem>
                    <FormLabel>Password</FormLabel>
                    <FormControl>
                        <Input placeholder="Password" {...field} />
                    </FormControl>
                    <FormMessage />
                    </FormItem>
                )}
                />
                <GoogleOauthButton/>
                <div className="flex justify-center">
                    <Button type="submit">Submit</Button>
                </div>
            </form>
        </Form>
    )
}