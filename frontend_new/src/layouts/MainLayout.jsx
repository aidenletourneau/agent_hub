import { Outlet } from "react-router";
import Navbar from "@/components/navbar";

export default function MainLayout() {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar/>


      <main className="flex-1 max-w-6xl mx-auto w-full px-4 py-6 flex justify-center items-center h-full">
        <Outlet />
      </main>

      <footer className="w-full bg-gray-100 py-4 text-center text-sm text-gray-600">
        Footer here
      </footer>
    </div>
  );
}