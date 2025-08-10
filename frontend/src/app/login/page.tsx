'use client';

import { useRouter } from 'next/navigation';
import { AuthForm } from '@/components/auth/auth-form';

export default function Login() {
  const router = useRouter();

  const handleLogin = async (formData: any) => {
    try {
      // In a real app, this would call your API
      console.log('Login data:', formData);
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Redirect to dashboard on success
      router.push('/dashboard');
    } catch (error) {
      throw new Error('Login failed. Please check your credentials.');
    }
  };

  return (
    <main className="container mx-auto px-4 py-8 pt-32">
      <AuthForm mode="login" onSubmit={handleLogin} />
    </main>
  );
}
