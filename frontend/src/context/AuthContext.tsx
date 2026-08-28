import React, { createContext, useContext, useState, useEffect } from 'react';
import type { UserProfile, UserRole } from '../types';
import { AuthService } from '../services/auth.service';

export type { UserRole } from '../types';

interface AuthContextType {
  user: UserProfile | null;
  role: UserRole;
  isAuthenticated: boolean;
  loginAsBanker: (employeeId?: string, password?: string) => Promise<void>;
  loginAsApplicant: (email?: string, password?: string) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<UserProfile | null>(null);

  useEffect(() => {
    AuthService.getCurrentSession().then(session => {
      if (session) setUser(session);
    });
  }, []);

  const loginAsBanker = async (employeeId = 'BKR-7749-NY', password = 'password') => {
    const profile = await AuthService.loginAsBanker(employeeId, password);
    setUser(profile);
  };

  const loginAsApplicant = async (email = 'alex.mercer@apextech.com', password = 'password') => {
    const profile = await AuthService.loginAsApplicant(email, password);
    setUser(profile);
  };

  const logout = async () => {
    await AuthService.logout();
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        role: user?.role || null,
        isAuthenticated: !!user,
        loginAsBanker,
        loginAsApplicant,
        logout
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
