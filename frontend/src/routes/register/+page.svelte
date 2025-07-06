<script lang="ts">
  import InputField from '$lib/components/InputField.svelte';
  import Button from '$lib/components/Button.svelte';
  import { registerSchema } from '$lib/schema/auth';
  import { apiFetch } from '$lib/utils/api';

  let email = '';
  let password = '';
  let role = 'REPORTER';
  let errors: Record<string, string> = {};

  async function handleSubmit() {
    const parsed = registerSchema.safeParse({ email, password, role });
    if (!parsed.success) {
      errors = {};
      for (const issue of parsed.error.issues) {
        errors[issue.path[0]] = issue.message;
      }
      return;
    }

    try {
      await apiFetch('/auth/register', {
        method: 'POST',
        body: JSON.stringify({ email, password, role }),
      });
      window.location.href = '/login';
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
    <h2 class="text-3xl font-bold text-center text-white">Register for Trybit</h2>
    <p class="text-center text-gray-400 text-sm mb-4">Create an account to track and manage issues.</p>

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

    <div class="space-y-1">
      <label for="role-select" class="block text-sm font-medium text-gray-300">Role</label>
      <select id="role-select" bind:value={role} class="w-full border border-gray-700 bg-gray-800 text-white rounded p-2 focus:outline-none">
        <option value="REPORTER">Reporter</option>
        <option value="MAINTAINER">Maintainer</option>
        <option value="ADMIN">Admin</option>
      </select>
      {#if errors.role}
        <p class="text-red-500 text-sm">{errors.role}</p>
      {/if}
    </div>

    <Button text="Register"/>

    <p class="text-sm text-center text-gray-400 mt-6">
      Already have an account? 
      <a href="/login" class="text-blue-400 hover:text-blue-300 underline ml-1">Login</a>
    </p>
  </form>
</div>