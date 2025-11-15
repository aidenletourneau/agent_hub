import { useAuth } from "@/contexts/AuthContext"

export default function ProfilePage(){
    const { user } = useAuth()

    return (
        <div>
            <h1>Email: {user.email}</h1><br/>
            <h1>Id: {user.id}</h1><br/>
            <h1>Username: {user.username}</h1>
        </div>

    )
}