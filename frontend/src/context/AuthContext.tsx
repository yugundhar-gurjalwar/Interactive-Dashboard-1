import { createContext, useState, useContext, useEffect, type ReactNode } from 'react';
import api from '../services/api';

interface User {
    id: number;
    email: string;
    is_active: boolean;
    is_superuser: boolean;
}

interface AuthContextType {
    user: User | null;
    login: (token: string) => void;
    logout: () => void;
    isAuthenticated: boolean;
    loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        initAuth();
    }, []);

    const initAuth = async () => {
        const token = localStorage.getItem('token');
        if (token) {
            try {
                const response = await api.get('/auth/me');
                setUser(response.data);
                setLoading(false);
                return;
            } catch (error) {
                console.log("Token invalid, falling back to guest login");
                localStorage.removeItem('token');
            }
        }
        await loginGuest();
    };

    const loginGuest = async () => {
        try {
            const response = await api.post('/auth/login/guest');
            localStorage.setItem('token', response.data.access_token);
            await fetchUser();
        } catch (error) {
            console.error("Failed to login as guest", error);
            setLoading(false);
        }
    };

    const fetchUser = async () => {
        try {
            const response = await api.get('/auth/me');
            setUser(response.data);
        } catch (error) {
            console.error("Failed to fetch user", error);
            localStorage.removeItem('token');
        } finally {
            setLoading(false);
        }
    };

    const login = (token: string) => {
        localStorage.setItem('token', token);
        fetchUser();
    };

    const logout = () => {
        // No-op or reset to guest if needed, but for "no login page" app, we keep user logged in.
        // localStorage.removeItem('token');
        // setUser(null);
        console.log("Logout disabled for single-user mode.");
    };

    return (
        <AuthContext.Provider value={{ user, login, logout, isAuthenticated: !!user, loading }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};
