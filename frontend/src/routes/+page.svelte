<script lang="ts">
  import { goto } from '$app/navigation';
    import SeverityChart from '$lib/components/SeverityChart.svelte';
  import { token, userRole } from '$lib/store';
  import { onMount } from 'svelte';
  import { get } from 'svelte/store';

  let loggedIn = !!get(token);
  let role = get(userRole) || 'GUEST';

  onMount(() => {
  if (!loggedIn) {
    goto('/login');
  }
});
</script>

<div class="min-h-screen bg-gray-950 text-white px-6 py-12">
  <div class="max-w-4xl mx-auto">
    {#if loggedIn}
      <h1 class="text-4xl font-bold mb-4">Welcome back<span class="text-blue-400">{" "} {role}</span> 👋</h1>
      <p class="text-gray-400 mb-8">You're logged in as a <span class="text-green-400 font-semibold">{role}</span>. Use the links below to navigate.</p>

      <div class="grid md:grid-cols-2 gap-6">
        {#if role === 'REPORTER'}
          <a href="/issues/create" class="block bg-blue-600 hover:bg-blue-700 transition p-5 rounded-xl shadow-xl">
            <h2 class="text-xl font-semibold mb-2">+ Report New Issue</h2>
            <p class="text-sm text-gray-200">Create a new issue with markdown support.</p>
          </a>

          <a href="/issues" class="block bg-gray-800 hover:bg-gray-700 transition p-5 rounded-xl shadow-xl">
            <h2 class="text-xl font-semibold mb-2">View My Issues</h2>
            <p class="text-sm text-gray-300">Check status, severity, and progress.</p>
          </a>
        {:else if role === 'MAINTAINER'}
          <SeverityChart />
          <a href="/issues" class="block bg-purple-700 hover:bg-purple-800 transition p-5 rounded-xl shadow-xl">
            <h2 class="text-xl font-semibold mb-2">Manage Assigned Issues</h2>
            <p class="text-sm text-gray-200">Track and update issue statuses.</p>
          </a>
        {:else if role === 'ADMIN'}
        <SeverityChart />
          <a href="/issues" class="block bg-red-600 hover:bg-red-700 transition p-5 rounded-xl shadow-xl">
            <h2 class="text-xl font-semibold mb-2">View All Issues</h2>
            <p class="text-sm text-gray-200">Complete access to all reported issues.</p>
          </a>
          <a href="/issues/create" class="block bg-gray-800 hover:bg-gray-700 transition p-5 rounded-xl shadow-xl">
            <h2 class="text-xl font-semibold mb-2">Create Issue</h2>
            <p class="text-sm text-gray-300">Create new issue.</p>
          </a>
        {/if}
      </div>
    {:else}
      <h1 class="text-4xl font-bold mb-4">Welcome to <span class="text-blue-500">Issue Tracker</span> 🚀</h1>
      <p class="text-gray-400 mb-8">Track, manage, and resolve issues with role-based access and real-time updates.</p>

      <div class="flex gap-4">
        <a href="/login" class="bg-blue-600 hover:bg-blue-700 transition px-6 py-3 rounded-lg text-white font-semibold shadow-lg">
          Login
        </a>
        <a href="/register" class="border border-blue-600 hover:bg-blue-600 transition px-6 py-3 rounded-lg text-blue-400 hover:text-white font-semibold shadow-lg">
          Register
        </a>
      </div>

      <ul class="mt-12 text-sm text-gray-500 space-y-2">
        <li>✅ Secure login and JWT-based auth</li>
        <li>✅ Markdown support for issue descriptions</li>
        <li>✅ Role-based permissions (REPORTER, MAINTAINER, ADMIN)</li>
        <li>✅ Beautiful dark mode UI</li>
      </ul>
    {/if}
  </div>
</div>
