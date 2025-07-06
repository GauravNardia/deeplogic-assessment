<script lang="ts">
  import InputField from '$lib/components/InputField.svelte';
  import Button from '$lib/components/Button.svelte';
  import { loginSchema } from '$lib/schema/auth';
  import { apiFetch } from '$lib/utils/api';
  import { token, userRole } from '$lib/store';

  let email = '';
  let password = '';
  let errors: Record<string, string> = {};

  async function handleSubmit() {
    const parsed = loginSchema.safeParse({ email, password });
    if (!parsed.success) {
      errors = {};
      for (const issue of parsed.error.issues) {
        errors[issue.path[0]] = issue.message;
      }
      return;
    }

    try {
      const res = await apiFetch('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      });

      console.log("Login response:", res); 

      token.set(res.access_token);
      userRole.set(res.user.role); 
      localStorage.setItem('token', res.access_token);
      localStorage.setItem('role', res.user.role);
      window.location.href = '/issues';
    } catch (err: any) {
      alert(err.message);
    }
  }
</script>

<div class="min-h-screen flex items-center justify-center bg-gray-950 px-4 py-12 text-white">
  <form
    on:submit|preventDefault={handleSubmit}
    class="w-full max-w-sm p-8 bg-gray-900 rounded-2xl shadow-2xl space-y-6 border border-gray-800"
  >
    <h2 class="text-3xl font-bold text-center text-white">Login to your account</h2>
    <p class="text-center text-gray-400 text-sm mb-4">Welcome back! Please enter your credentials.</p>

    <InputField
      label="Email"
      type="email"
      placeholder="your@email.com"
      value={email}
      error={errors.email}
      onInput={(val) => email = val}
    />

    <InputField
      label="Password"
      type="password"
      placeholder="********"
      value={password}
      error={errors.password}
      onInput={(val) => password = val}
    />

    <Button text="Login"/>

    <p class="text-sm text-center text-gray-400 mt-6">
      Don't have an account? 
      <a href="/register" class="text-blue-400 hover:text-blue-300 underline ml-1">Register</a>
    </p>
  </form>
</div>
