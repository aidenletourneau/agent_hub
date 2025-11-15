import './App.css'
import HomePage from "./pages/HomePage"
import LoginPage from "./pages/LoginPage"
import RegisterPage from "./pages/RegisterPage"
import MainLayout from "./layouts/MainLayout";
import AgentsPage from './pages/AgentsPage';
import { BrowserRouter, Routes, Route } from "react-router";
import ProfilePage from './pages/ProfilePage';
import { AuthProvider } from './contexts/AuthContext';
import RequireAuth from './RequireAuth';


function App() {


  return (
    <AuthProvider >
      <BrowserRouter>
        <Routes>
          <Route element={<MainLayout />}>
            <Route index element={<HomePage />} />
            <Route path="login" element={<LoginPage />} />
            <Route path="register" element={<RegisterPage />} />


            {/* Logged In Routes */}
            <Route element={<RequireAuth/>}>
              <Route path="profile" element={<ProfilePage />} />
              <Route path="agents" element={<AgentsPage />} />
            </Route>
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App
