import { NavLink } from "react-router";
import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
} from "@/components/ui/navigation-menu"
import LogoutButton from "./logoutbutton";
import { useAuth } from "@/contexts/AuthContext"


export default function Navbar() {
    const { user } = useAuth()

    return (
    <div className="w-full bg-white shadow-sm border-b flex justify-between items-center px-4">
        <h1 className="text-xl font-bold">Agent-Hub</h1>
        <NavigationMenu className="max-w-6xl mx-auto ">
          <NavigationMenuList className="flex flex-row items-center gap-6 h-16">
            <NavigationMenuItem>
              <NavigationMenuLink asChild>
                <NavLink to="/" end>Home</NavLink>
              </NavigationMenuLink>
            </NavigationMenuItem>
            {user ? (
              <>
                <NavigationMenuItem>
                  <NavigationMenuLink asChild>
                    <NavLink to="/profile" end>Profile</NavLink>
                  </NavigationMenuLink>
                </NavigationMenuItem>
                <NavigationMenuItem>
                  <NavigationMenuLink asChild>
                    <NavLink to="/agents" end>My Agents</NavLink>
                  </NavigationMenuLink>
                </NavigationMenuItem>
              </>
            ) : (
              <NavigationMenuItem>
                <NavigationMenuLink asChild>
                  <NavLink to="/login" end>Login</NavLink>
                </NavigationMenuLink>
              </NavigationMenuItem>
            )}

          </NavigationMenuList>
        </NavigationMenu>
        {user && (<LogoutButton/>)}
        
      </div>
    )
}