import type { UserProfile, UserRole } from '../types';
import { apiClient } from '../api/client';

export class AuthService {
  static async login(email: string, password = 'password'): Promise<{ userProfile: UserProfile; tokens: any }> {
    try {
      const response = await apiClient.post('/auth/login', { email, password });
      const { access_token, refresh_token, user } = response.data;

      if (access_token) {
        localStorage.setItem('access_token', access_token);
      }
      if (refresh_token) {
        localStorage.setItem('refresh_token', refresh_token);
      }

      const role: UserRole = user?.role === 'banker' ? 'banker' : 'applicant';
      const userProfile: UserProfile = {
        id: String(user?.id || (role === 'banker' ? 'BKR-7749-NY' : 'APP-8942-NY')),
        name: user?.name || (role === 'banker' ? 'Vikram Singh' : 'Alex Mercer'),
        role,
        title: role === 'banker' ? 'Lead Underwriter / Risk Officer' : 'CFO, Apex Tech Corp',
        email: user?.email || email,
        authLevel: role === 'banker' ? 'L3-AUTH' : undefined,
        accountStatus: 'VERIFIED',
      };

      localStorage.setItem('agenttrust_auth_user', JSON.stringify(userProfile));
      return { userProfile, tokens: response.data };
    } catch (err: any) {
      console.error('Authentication Error:', err);
      // Remove stale user token state
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      
      const errorMsg = err.response?.data?.detail || err.response?.data?.error?.message || err.message || 'Authentication failed.';
      throw new Error(typeof errorMsg === 'string' ? errorMsg : 'Authentication failed.');
    }
  }

  static async loginAsBanker(employeeId = 'BKR-7749-NY', password = 'password'): Promise<UserProfile> {
    const res = await this.login(employeeId.includes('@') ? employeeId : 'banker@agenttrust.bank', password);
    return res.userProfile;
  }

  static async loginAsApplicant(email = 'alex.mercer@apextech.com', password = 'password'): Promise<UserProfile> {
    const res = await this.login(email, password);
    return res.userProfile;
  }

  static async getCurrentSession(): Promise<UserProfile | null> {
    const saved = localStorage.getItem('agenttrust_auth_user');
    if (!saved) return null;
    try {
      return JSON.parse(saved);
    } catch {
      return null;
    }
  }

  static async logout(): Promise<void> {
    try {
      await apiClient.post('/auth/logout');
    } catch {
      // Ignore network errors on logout
    } finally {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('agenttrust_auth_user');
    }
  }
}
